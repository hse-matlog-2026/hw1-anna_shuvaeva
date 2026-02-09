import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

print("=== Тест parse() ===")

tests = ['x', 'T', '~p', '(p&q)', 'x13', '(x|y)', '~~~x']

for string in tests:
    try:
        formula = Formula.parse(string)
        print(f"✓ parse('{string}') = {formula}")
        # Проверим, что строковое представление совпадает
        if str(formula) != string:
            print(f"  ВНИМАНИЕ: str(formula) = '{str(formula)}' != '{string}'")
    except Exception as e:
        print(f"✗ parse('{string}') -> Ошибка: {e}")
