import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

# Тест который падает в задании
test_cases = [
    'F',
    'T', 
    'x',
    '~x',
    '(x&y)',
    '(x|y)',
    '(x->y)',
    '(x+y)',
    '(x<->y)',
    '(x-&y)',
    '(x-|y)',
]

for s in test_cases:
    f = Formula.parse(s)
    print(f"\nTesting: {s}")
    try:
        result = f.to_not_and_or()
        print(f"  Result: {result}")
        print(f"  Operators: {result.operators()}")
        print(f"  Only &,|,~? {result.operators().issubset({'&', '|', '~'})}")
    except Exception as e:
        print(f"  ERROR: {e}")
