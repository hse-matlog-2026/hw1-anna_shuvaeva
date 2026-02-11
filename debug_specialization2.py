import sys
sys.path.insert(0, '.')
from propositions.proofs import *

# Воспроизведём тест
rule = InferenceRule([Formula.parse('(x|y)')], Formula.parse('(y|x)'))
specialization = InferenceRule([Formula.parse('(w|z)')], Formula.parse('(z|w)'))

print("=== Тест подстановки ===")
print(f"rule: {rule}")
print(f"specialization: {specialization}")
print(f"is specialization? {specialization.is_specialization_of(rule)}")

substitution = specialization.specialization_map(rule)
print(f"\nsubstitution dict: {substitution}")
print(f"type: {type(substitution)}")

# Проверим подстановку для формулы (x|y)
formula = Formula.parse('(x|y)')
print(f"\nИсходная формула: {formula}")
print(f"Подстановка x -> {substitution.get('x', 'NO KEY')}")
print(f"Подстановка y -> {substitution.get('y', 'NO KEY')}")

new_formula = formula.substitute_variables(substitution)
print(f"Результат подстановки: {new_formula}")
