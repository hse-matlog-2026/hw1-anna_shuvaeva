import sys
sys.path.insert(0, '.')
from propositions.syntax import Formula
from propositions.proofs import InferenceRule

general = Formula.parse('(~p->~(q|T))')
special = Formula.parse('(~(x|y)->~((z&(w->~z))|T))')

print(f"General: {general}")
print(f"Special: {special}")

result = InferenceRule._formula_specialization_map(general, special)
print(f"Result: {result}")

# Отладка шаг за шагом
print("\nОтладка структуры:")
print(f"general.root: {general.root}")
print(f"special.root: {special.root}")
print(f"general.first: {general.first}")
print(f"special.first: {special.first}")
print(f"general.second: {general.second}")
print(f"special.second: {special.second}")
