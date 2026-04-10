from django.shortcuts import get_object_or_404, redirect

from .models import Recipe


def redirect_to_recipe(request, code):
    recipe = get_object_or_404(Recipe, short_code=code)
    return redirect(f'/recipes/{recipe.id}')
