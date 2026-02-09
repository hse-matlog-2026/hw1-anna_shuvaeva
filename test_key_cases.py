import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

test_cases = [
    ('x', 'x', ''),
    ('T', 'T', ''),
    ('F', 'F', ''),
    ('x2', 'x2', ''),
    ('x12', 'x12', ''),
    ('~p', '~p', ''),
    ('(p&q)', '(p&q)', ''),
    ('x|y', 'x', '|y'),
    ('a', None, 'Invalid formula: a'),
    (')', None, 'Invalid formula: )'),
    ('(x&y', None, "Expected ')', got ''"),
    ('(T)', None, "Expected operator, got ')'"),
]

print("=== Ключевые тесты ===")
all_ok = True

for string, exp_formula, exp_rest in test_cases:
    formula, rest = Formula._parse_prefix(string)
    
    ok = True
    if formula != exp_formula:
        print(f"✗ '{string}': формула {formula} != {exp_formula}")
        ok = False
    if rest != exp_rest:
        print(f"✗ '{string}': остаток '{rest}' != '{exp_rest}'")
        ok = False
    
    if ok:
        print(f"✓ '{string}' -> OK")
    else:
        all_ok = False

if all_ok:
    print("\n✅ Все ключевые тесты прошли!")
else:
    print("\n❌ Есть ошибки!")
