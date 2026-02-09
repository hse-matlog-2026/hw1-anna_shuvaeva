def prove_specialization(proof: Proof, specialization: InferenceRule) -> Proof:
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
            # It should still be an assumption in the specialized proof
            specialized_lines.append(Proof.Line(specialized_formula, None, None))
        else:
            # This was a rule application
            # Keep the same rule, but specialize the assumptions
            specialized_lines.append(
                Proof.Line(
                    specialized_formula,
                    line.rule,  # Same rule
                    line.assumptions  # Same assumption line numbers
                )
            )
    
    # Create the specialized proof
    # Note: The rules remain the same
    return Proof(specialization, proof.rules, specialized_lines)
