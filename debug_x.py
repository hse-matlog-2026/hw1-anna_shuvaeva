import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula, is_variable

print("=== Отладка парсинга 'x' ===")
string = "x"
print(f"Строка: '{string}'")
print(f"string[0] = '{string[0]}'")
print(f"'p' <= '{string[0]}' <= 'z' ? {'p' <= string[0] <= 'z'}")
print(f"is_variable('{string[0]}') = {is_variable(string[0])}")

# Проверим функцию is_variable
print("\n=== Проверка is_variable ===")
test_vars = ['x', 'y', 'z', 'p', 'q', 'r', 'x1', 'x12', 'p3']
for var in test_vars:
    print(f"is_variable('{var}') = {is_variable(var)}")

# Попробуем распарсить
print("\n=== Парсинг ===")
formula, rest = Formula._parse_prefix("x")
print(f"Результат: formula={formula}, rest='{rest}'")
