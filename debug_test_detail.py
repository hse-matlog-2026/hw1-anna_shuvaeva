import sys
sys.path.insert(0, '.')
from propositions.semantics import all_models
from logic_utils import frozendict

# Воспроизводим тест из semantics_test.py
variables1 = ('p', 'q')
models1 = [
    frozendict({'p': False, 'q': False}),
    frozendict({'p': False, 'q': True}),
    frozendict({'p': True, 'q': False}),
    frozendict({'p': True, 'q': True})
]

variables2 = ['x']
models2 = [frozendict({'x': False}), frozendict({'x': True})]

variables3 = ('q', 'p')
models3 = [
    frozendict({'q': False, 'p': False}),
    frozendict({'q': False, 'p': True}),
    frozendict({'q': True, 'p': False}),
    frozendict({'q': True, 'p': True})
]

print("=== Тест 1: variables = ('p', 'q') ===")
result1 = all_models(variables1)
print(f"Результат: {result1}")
print(f"Ожидается: {models1}")
print(f"Совпадают? {result1 == models1}")

print("\n=== Тест 2: variables = ['x'] ===")
result2 = all_models(variables2)
print(f"Результат: {result2}")
print(f"Ожидается: {models2}")
print(f"Совпадают? {result2 == models2}")

print("\n=== Тест 3: variables = ('q', 'p') ===")
result3 = all_models(variables3)
print(f"Результат: {result3}")
print(f"Ожидается: {models3}")
print(f"Совпадают? {result3 == models3}")

# Проверка отдельных элементов
print("\n=== Детальная проверка теста 3 ===")
print("Порядок ключей в result3[0]:", list(result3[0].keys()))
print("Порядок ключей в models3[0]:", list(models3[0].keys()))
