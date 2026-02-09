import sys
sys.path.insert(0, '.')
from propositions.proofs import Proof, InferenceRule
from propositions.syntax import Formula

# Воссоздаем полный proof из теста
rule1 = InferenceRule([Formula.parse('~~p')], Formula.parse('p'))
rule2 = InferenceRule([Formula.parse('p'), Formula.parse('~~p')], Formula.parse('~~~~p'))

# Создаем lines как в тесте (из вывода видно 4 строки)
lines = [
    Proof.Line(Formula.parse('x'), None, None),      # 0: x (assumption)
    Proof.Line(Formula.parse('p'), rule1, [0]),      # 1: p from rule1 on line 0
    Proof.Line(Formula.parse('~~x'), None, None),    # 2: ~~x (assumption)
    Proof.Line(Formula.parse('x'), rule1, [2]),      # 3: x from rule1 on line 2
]

statement = InferenceRule([Formula.parse('x'), Formula.parse('~~~~x')], 
                          Formula.parse('r'))

proof = Proof(statement, {rule1, rule2}, lines)

print("=== Полная проверка proof ===")
print(f"Statement: {statement}")
print(f"Rules: {proof.rules}")
print(f"Number of lines: {len(lines)}")

print("\n=== Проверка каждой строки ===")
for i in range(len(lines)):
    line = lines[i]
    print(f"\n--- Строка {i}: {line.formula} ---")
    
    if line.rule:
        print(f"  rule: {line.rule}")
        print(f"  assumptions: {line.assumptions}")
        
        inferred = proof.rule_for_line(i)
        print(f"  inferred_rule: {inferred}")
        
        if inferred:
            print(f"  inferred.is_specialization_of(line.rule): {inferred.is_specialization_of(line.rule)}")
            print(f"  line.rule.is_specialization_of(inferred): {line.rule.is_specialization_of(inferred)}")
            
            # Проверяем allowed rules
            allowed = False
            for r in proof.rules:
                if line.rule == r or line.rule.is_specialization_of(r):
                    allowed = True
                    print(f"  line.rule allowed via rule: {r}")
                    break
            
            # Проверяем рекурсивно assumptions
            print(f"  Проверка assumption lines:")
            for a in line.assumptions:
                print(f"    Строка {a}: valid={proof.is_line_valid(a)}")
    
    print(f"  is_line_valid({i}) = {proof.is_line_valid(i)}")
    
    # Что ожидает тест? Нужно посмотреть в тесте
    # Давайте попробуем угадать: строка 0: True, строка 1: False, строка 2: True, строка 3: True
    expected = [True, False, True, True]
    print(f"  Ожидается примерно: {expected[i]}")
