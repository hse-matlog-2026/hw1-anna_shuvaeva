import sys
sys.path.insert(0, '.')
from propositions.semantics import all_models
from logic_utils import frozendict

# Протестируем все_модели
print("=== Тест all_models(['p', 'q']) ===")
result = all_models(['p', 'q'])
print(f"Результат: {result}")
print(f"Количество моделей: {len(result)}")

# Проверим ожидаемый результат
expected = [
    {'p': False, 'q': False},
    {'p': False, 'q': True},
    {'p': True, 'q': False},
    {'p': True, 'q': True}
]
print(f"\nОжидалось: {expected}")

# Проверим поэлементно
print("\nПроверка:")
for i, (res, exp) in enumerate(zip(result, expected)):
    if res == exp:
        print(f"  Модель {i}: ✓ {res}")
    else:
        print(f"  Модель {i}: ✗ {res} != {exp}")

# Проверим тип моделей
print(f"\nТип моделей: {type(result[0]) if result else 'N/A'}")
print("Ожидается: dict (или возможно frozendict)")

# Проверим порядок ключей
print("\nПорядок ключей в моделях:")
for model in result:
    print(f"  {list(model.keys())}")
