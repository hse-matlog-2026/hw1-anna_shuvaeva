import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

tests = [
    ('x', 'OK'),
    ('T', 'OK'),
    ('a', 'Invalid formula: a'),
    (')', 'Invalid formula: )'),
    ('x&', 'x, &'),
    ('p3&y', 'p3, &y'),
    ('F)', 'F, )'),
    ('~x', '~x, '),
    ('x12', 'x12, '),
    ('(p&q)', '(p&q), '),
]

print("=== Финальный тест ===")
for string, expected in tests:
    formula, rest = Formula._parse_prefix(string)
    print(f"'{string}' -> formula={formula}, rest='{rest}'")
