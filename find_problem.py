import sys
sys.path.insert(0, '.')
from propositions.operators_test import many_fs
from propositions.syntax import Formula, to_not_and_or

print(f"Всего формул для теста: {len(many_fs)}")

for i, s in enumerate(many_fs[:10]):  # Проверим первые 10
    print(f"\n{i}. Формула: '{s}'")
    f = Formula.parse(s)
    ff = to_not_and_or(f)
    if ff is None:
        print(f"  ❌ to_not_and_or вернула None!")
        break
    else:
        print(f"  ✅ Результат: {ff}")
