# author Глінський Артем Валерійович
import functools , time

# Список із публічних об'єктів для експорту
__all__ = ['pretty_print', 'error_handler', 'parse_input']

# Функція для кольоро-анімованого виведення тексту
# colrama не викоростина
def pretty_print(text, color='cyan', delay=0.04):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    for char in text:
        colored_text = colors.get(color.lower(), colors) + char + colors['reset']
        print(colored_text, end='', flush=True)
        time.sleep(delay)
    print()

# Декоратор краси ))) на майбутне
# def pretty_decor(color='cyan'):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             result = func(*args, **kwargs)
#             pretty_print(result, color)
#         return wrapper
#     return decorator

# Декоратор обробки помилок
def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pretty_print(f"An error occurred in function '{func.__name__}': {e}", 'red')
    return wrapper

# парсер вводу
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args
