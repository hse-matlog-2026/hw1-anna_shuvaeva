import sys
sys.path.insert(0, '.')
from propositions.proofs import Proof, InferenceRule
from propositions.syntax import Formula

# Проверяем что методы есть
proof = Proof(
    InferenceRule([Formula.parse('x')], Formula.parse('x')),
    set(),
    [Proof.Line(Formula.parse('x'), None, None)]
)

print("is_line_valid существует:", hasattr(proof, 'is_line_valid'))
print("is_valid существует:", hasattr(proof, 'is_valid'))

if hasattr(proof, 'is_line_valid'):
    try:
        result = proof.is_line_valid(0)
        print(f"is_line_valid(0) работает, возвращает: {result}")
    except Exception as e:
        print(f"is_line_valid(0) ошибка: {type(e).__name__}: {e}")

if hasattr(proof, 'is_valid'):
    try:
        result = proof.is_valid()
        print(f"is_valid() работает, возвращает: {result}")
    except Exception as e:
        print(f"is_valid() ошибка: {type(e).__name__}: {e}")
