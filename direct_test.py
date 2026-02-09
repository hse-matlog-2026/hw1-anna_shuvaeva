import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

# Тест из syntax_test.py для 'x'
print("=== Тест для 'x' ===")
formula, remainder = Formula._parse_prefix('x')
print(f"formula = {formula}")
print(f"remainder = '{remainder}'")

# Что должно быть по тесту
expected_formula = Formula('x')
expected_remainder = ''
print(f"\nОжидалось:")
print(f"  formula = {expected_formula}")
print(f"  remainder = '{expected_remainder}'")

# Проверки
print(f"\nПроверки:")
print(f"  formula is None? {formula is None}")
print(f"  formula == expected_formula? {formula == expected_formula}")
print(f"  remainder == expected_remainder? {remainder == expected_remainder}")
print(f"  str(formula) = '{str(formula)}'")
print(f"  str(expected_formula) = '{str(expected_formula)}'")

if formula is None:
    print("ОШИБКА: формула None!")
elif formula != expected_formula:
    print("ОШИБКА: формулы не равны!")
elif remainder != expected_remainder:
    print(f"ОШИБКА: остаток '{remainder}' != '{expected_remainder}'")
else:
    print("✓ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
