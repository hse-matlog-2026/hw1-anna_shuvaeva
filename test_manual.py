import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

print("=== Ручная проверка is_formula ===")

# Простые тесты
tests = [
    ('', False),      # пустая строка
    ('x', True),      # переменная
    ('T', True),      # константа
    ('~p', True),     # унарная формула
    ('(p&q)', True),  # бинарная формула
    ('x&', False),    # неполная формула
    ('a', False),     # не переменная
]

for string, expected in tests:
    result = Formula.is_formula(string)
    status = '✓' if result == expected else '✗'
    print(f"{status} is_formula('{string}') = {result} (ожидалось: {expected})")
