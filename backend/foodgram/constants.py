from django.core.validators import RegexValidator

# Пагинация
BASIC_PAGE_SIZE = 6
MAX_LIMIT_PAGE_SIZE = 100

# Ограничения длины
EMAIL_MAX_LENGTH = 254
USERNAME_MAX_LENGTH = 150
NAME_MAX_LENGTH = 150

TAG_NAME_MAX_LENGTH = 32

INGREDIENT_NAME_MAX_LENGTH = 128
INGREDIENT_MEASURE_MAX_LENGTH = 64
COLOR_NAME_MAX_LENGTH = 7

RECIPE_NAME_MAX_LENGTH = 256

UUID_MAX_LENGTH = 22

COOKING_TIME_MIN = 1
COOKING_TIME_MAX = 1440

INGREDIENT_MIN_AMOUNT = 1
INGREDIENT_MAX_AMOUNT = 1000

# Регулярное выражение для пользователя
USERNAME_REGEX = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message=(
        'Имя пользователя может содержать только буквы, '
        'цифры и символы @/./+/-/_'
    )
)
