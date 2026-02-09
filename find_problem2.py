import sys
sys.path.insert(0, '.')
from propositions.operators_test import many_fs
from propositions.syntax import Formula, to_not_and_or

print(f"Всего формул для теста: {len(many_fs)}")

for i, s in enumerate(many_fs):
    f = Formula.parse(s)
    ff = to_not_and_or(f)
    if ff is None:
        print(f"\n❌ Найдена проблема! Формула {i}: '{s}'")
        print(f"   parsed: {f}")
        print(f"   to_not_and_or: {ff}")
        break
    elif i >= 10:  # Покажем только после 10-й
        print(f"  {i}. '{s}' -> OK")
