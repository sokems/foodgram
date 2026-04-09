from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.serializers.recipe_mini import RecipeMiniSerializer

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name',
            'avatar', 'is_subscribed',
        )
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.subscribers.filter(user=request.user).exists()
        )

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара."""

    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)

    def to_representation(self, instance):
        return {
            'avatar': instance.avatar.url
            if instance.avatar else None
        }


class SubscriptionSerializer(UserProfileSerializer):
    """Сериализатор отображения подписок и рецептов автора."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta(UserProfileSerializer.Meta):
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name',
            'avatar', 'is_subscribed',
            'recipes', 'recipes_count',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = (
            request.query_params.get('recipes_limit')
            if request else None
        )
        queryset = obj.recipes.all()
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]
        return RecipeMiniSerializer(queryset, many=True).data
