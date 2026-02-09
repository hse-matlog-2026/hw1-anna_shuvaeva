import sys
sys.path.insert(0, '.')
from propositions.semantics import all_models

# Простой тест
print("Тест all_models(['p', 'q']):")
result = all_models(['p', 'q'])
print(f"Результат: {result}")
print(f"Тип первого элемента: {type(result[0])}")
