import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

print("=== Отладка 'x13->x14' ===")

# Парсим
formula, rest = Formula._parse_prefix('x13->x14')
print(f"Результат: formula={formula}, rest='{rest}'")

# Что должно быть
expected_formula = Formula('x13')
expected_rest = '->x14'
print(f"Ожидается: formula={expected_formula}, rest='{expected_rest}'")

# Проверяем
if formula != expected_formula:
    print(f"ОШИБКА: формулы не равны")
    print(f"  str(formula)='{str(formula)}'")
    print(f"  str(expected_formula)='{str(expected_formula)}'")
    
if rest != expected_rest:
    print(f"ОШИБКА: остаток '{rest}' != '{expected_rest}'")

# Проверим is_variable
print(f"\nis_variable('x13') = {Formula.is_variable('x13')}")
print(f"is_variable('x1') = {Formula.is_variable('x1')}")
print(f"is_variable('x') = {Formula.is_variable('x')}")
