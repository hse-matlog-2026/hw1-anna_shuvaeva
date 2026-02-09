import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

# Воспроизведем тест для x13->x14
print("=== Тест для 'x13->x14' ===")

# Парсим
result = Formula._parse_prefix('x13->x14')
print(f"Результат парсинга: {result}")

# Ожидаемый результат
expected = (Formula('x13'), '->x14')
print(f"Ожидаемый результат: {expected}")

# Проверка
if result == expected:
    print("✓ Тест прошел!")
else:
    print("✗ Тест не прошел!")
    print(f"  result[0] == expected[0] ? {result[0] == expected[0]}")
    print(f"  result[1] == expected[1] ? {result[1] == expected[1]}")
    print(f"  result[0]: {result[0]}, str: '{str(result[0])}'")
    print(f"  expected[0]: {expected[0]}, str: '{str(expected[0])}'")
