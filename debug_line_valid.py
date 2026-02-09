import sys
sys.path.insert(0, '.')
from propositions.proofs import Proof, InferenceRule
from propositions.syntax import Formula

# Воссоздаем proof из теста
rules = {
    InferenceRule([Formula.parse('~~p')], Formula.parse('p')),
    InferenceRule([Formula.parse('p'), Formula.parse('~~p')], Formula.parse('~~~~p'))
}
lines = [
    Proof.Line(Formula.parse('x'), None, None),  # line 0: предположение
    Proof.Line(Formula.parse('p'), rules[0], [0]),  # line 1: правило ['~~p'] ==> 'p' на строке 0
]
statement = InferenceRule([Formula.parse('x'), Formula.parse('~~~~x')], 
                          Formula.parse('r'))

proof = Proof(statement, rules, lines)

print("Тестируем is_line_valid:")
for i in range(len(lines)):
    valid = proof.is_line_valid(i)
    print(f"  Строка {i}: {lines[i]}")
    print(f"    is_line_valid = {valid}")
    
    if i == 1:
        line = lines[1]
        print(f"    line.rule: {line.rule}")
        print(f"    line.assumptions: {line.assumptions}")
        print(f"    rule_for_line(1): {proof.rule_for_line(1)}")
        
        # Проверяем специализацию
        inferred = proof.rule_for_line(1)
        if inferred:
            print(f"    Специализация line.rule -> inferred: {line.rule.specialization_map(inferred)}")
            print(f"    Специализация inferred -> line.rule: {inferred.specialization_map(line.rule)}")
