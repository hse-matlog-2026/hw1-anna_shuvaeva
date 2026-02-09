import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula

# Простой тест
f = Formula.parse('F')
print(f"Formula: {f}")
print(f"Type: {type(f)}")

result = f.to_not_and_or()
print(f"Result: {result}")
print(f"Result type: {type(result)}")
