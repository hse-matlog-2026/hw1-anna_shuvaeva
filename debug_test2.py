import sys
sys.path.insert(0, '.')
from propositions.proofs import Proof, InferenceRule
from propositions.syntax import Formula

# Воссоздаем тестовый proof
rule1 = InferenceRule([Formula.parse('~~p')], Formula.parse('p'))
rule2 = InferenceRule([Formula.parse('p'), Formula.parse('~~p')], Formula.parse('~~~~p'))

lines = [
    Proof.Line(Formula.parse('x'), None, None),      # 0: x
    Proof.Line(Formula.parse('p'), rule1, [0]),      # 1: p from ~~p->p on line 0
]

statement = InferenceRule([Formula.parse('x'), Formula.parse('~~~~x')], 
                          Formula.parse('r'))

proof = Proof(statement, {rule1, rule2}, lines)

print("Проверяем is_line_valid для строки 1 (p):")
print(f"Строка 0: {lines[0].formula}")
print(f"Строка 1: {lines[1].formula} с правилом {rule1}")
print(f"line.assumptions: {lines[1].assumptions}")

inferred = proof.rule_for_line(1)
print(f"\nrule_for_line(1): {inferred}")

print(f"\nПроверяем специализацию:")
print(f"rule1.is_specialization_of(inferred): {rule1.is_specialization_of(inferred)}")
print(f"inferred.is_specialization_of(rule1): {inferred.is_specialization_of(rule1)}")

print(f"\nПроверяем вхождения в statement.assumptions:")
print(f"Формула 'p' в statement.assumptions: {Formula.parse('p') in statement.assumptions}")
print(f"statement.assumptions: {statement.assumptions}")

print(f"\nТекущий is_line_valid(1): {proof.is_line_valid(1)}")
