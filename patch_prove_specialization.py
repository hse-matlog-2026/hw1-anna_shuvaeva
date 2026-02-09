import re

with open('propositions/some_proofs.py', 'r') as f:
    content = f.read()

# Находим старую функцию prove_specialization
pattern = r'def prove_specialization\(proof: Proof, specialization: InferenceRule\) -> Proof:.*?# Task 5\.1.*?def _inline_proof_once'
new_function = '''def prove_specialization(proof: Proof, specialization: InferenceRule) -> Proof:
    """Converts the given proof of an inference rule to a proof of the given
    specialization of that inference rule.

    Parameters:
        proof: valid proof to convert.
        specialization: specialization of the rule proven by the given proof.

    Returns:
        A valid proof of the given specialization via the same inference rules
        as the given proof.
    """
    assert proof.is_valid()
    assert specialization.is_specialization_of(proof.statement)
    # Task 5.1
    
    # Get the substitution map from proof.statement to specialization
    substitution = proof.statement.specialization_map(specialization)
    
    # Specialize all formulas in the proof
    specialized_lines = []
    for line in proof.lines:
        # Specialize the formula
        specialized_formula = line.formula.substitute_variables(substitution)
        
        if line.rule is None:
            # This was an assumption line
            specialized_lines.append(Proof.Line(specialized_formula, None, None))
        else:
            # This was a rule application
            specialized_lines.append(
                Proof.Line(
                    specialized_formula,
                    line.rule,
                    line.assumptions
                )
            )
    
    # Create the specialized proof
    return Proof(specialization, proof.rules, specialized_lines)

def _inline_proof_once'''

# Заменяем
new_content = re.sub(pattern, new_function, content, flags=re.DOTALL)

with open('propositions/some_proofs.py', 'w') as f:
    f.write(new_content)

print("Файл исправлен")
