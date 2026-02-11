# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2025
# File name: propositions/deduction.py

"""Useful proof manipulation maneuvers in Propositional Logic."""

from propositions.syntax import *
from propositions.proofs import *
from propositions.axiomatic_systems import *
import unittest

def prove_corollary(antecedent_proof: Proof, consequent: Formula,
                    conditional: InferenceRule) -> Proof:
    assert antecedent_proof.is_valid()
    assert InferenceRule([],
                         Formula('->', antecedent_proof.statement.conclusion,
                                 consequent)).is_specialization_of(conditional)
    implication = Formula('->', antecedent_proof.statement.conclusion, consequent)
    implication_proof = Proof(
        InferenceRule([], implication),
        {conditional, MP},
        [Proof.Line(implication, conditional, [])]
    )
    new_lines = []
    for line in antecedent_proof.lines:
        new_lines.append(line)
    new_lines.append(Proof.Line(implication, conditional, []))
    antecedent_line = len(antecedent_proof.lines) - 1
    implication_line = len(antecedent_proof.lines)
    
    new_lines.append(Proof.Line(
        consequent,
        MP,
        (antecedent_line, implication_line)
    ))
    new_rules = antecedent_proof.rules.union({MP, conditional})
    new_statement = InferenceRule(
        antecedent_proof.statement.assumptions,
        consequent
    )
    
    return Proof(new_statement, new_rules, new_lines)

def combine_proofs(antecedent1_proof: Proof, antecedent2_proof: Proof,
                   consequent: Formula, double_conditional: InferenceRule) -> \
        Proof:
    """Combines the given proofs of two formulas `antecedent1` and `antecedent2`
    into a proof of the given formula `consequent` by using the given
    assumptionless inference rule of which
    ``'(``\\ `antecedent1`\\ ``->(``\\ `antecedent2`\\ ``->``\\ `consequent`\\ ``))'``
    is a specialization.

    Parameters:
        antecedent1_proof: valid proof of `antecedent1`.
        antecedent2_proof: valid proof of `antecedent2` from the same
            assumptions and inference rules as `antecedent1_proof`.
        consequent: formula to prove.
        double_conditional: assumptionless inference rule of which the
            assumptionless inference rule with conclusion
            ``'(``\\ `antecedent1`\\ ``->(``\\ `antecedent2`\\ ``->``\\ `consequent`\\ ``))'``
            is a specialization.

    Returns:
        A valid proof of `consequent` from the same assumptions as the given
        proofs, via the same inference rules as the given proofs and in addition
        `~propositions.axiomatic_systems.MP` and `double_conditional`.
    """
    assert antecedent1_proof.is_valid()
    assert antecedent2_proof.is_valid()
    assert antecedent1_proof.statement.assumptions == \
           antecedent2_proof.statement.assumptions
    assert antecedent1_proof.rules == antecedent2_proof.rules
    assert InferenceRule(
        [], Formula('->', antecedent1_proof.statement.conclusion,
        Formula('->', antecedent2_proof.statement.conclusion, consequent))
        ).is_specialization_of(double_conditional)
    
    double_implication = Formula('->', 
        antecedent1_proof.statement.conclusion,
        Formula('->', antecedent2_proof.statement.conclusion, consequent)
    )

    new_lines = []
    for line in antecedent1_proof.lines:
        new_lines.append(line)
    
    antecedent1_line = len(antecedent1_proof.lines) - 1
    offset = len(antecedent1_proof.lines)
    
    for line in antecedent2_proof.lines:
        if line.rule is None:
            new_lines.append(line)
        else:
            adjusted_assumptions = tuple(a + offset for a in line.assumptions)
            new_lines.append(Proof.Line(
                line.formula,
                line.rule,
                adjusted_assumptions
            ))
    antecedent2_line = offset + len(antecedent2_proof.lines) - 1
    new_lines.append(Proof.Line(double_implication, double_conditional, []))
    double_implication_line = len(new_lines) - 1

    
    new_lines.append(Proof.Line(
        Formula('->', antecedent2_proof.statement.conclusion, consequent),
        MP,
        (antecedent1_line, double_implication_line)
    ))
    
    second_mp_line = len(new_lines) - 1 
    
    new_lines.append(Proof.Line(
        consequent,
        MP,
        (antecedent2_line, second_mp_line)
    ))
    
    new_rules = antecedent1_proof.rules.union({MP, double_conditional})
    new_statement = InferenceRule(
        antecedent1_proof.statement.assumptions,
        consequent
    )
    
    return Proof(new_statement, new_rules, new_lines)

def remove_assumption(proof: Proof) -> Proof:
    """Converts the given proof of some `conclusion` formula, the last
    assumption of which is an assumption `assumption`, to a proof of
    ``'(``\\ `assumption`\\ ``->``\\ `conclusion`\\ ``)'`` from the same assumptions
    except `assumption`.

    Parameters:
        proof: valid proof to convert, with at least one assumption, via some
            set of inference rules all of which have no assumptions except
            perhaps `~propositions.axiomatic_systems.MP`.

    Returns:
        A valid proof of ``'(``\\ `assumption`\\ ``->``\\ `conclusion`\\ ``)'``
        from the same assumptions as the given proof except the last one, via
        the same inference rules as the given proof and in addition
        `~propositions.axiomatic_systems.MP`,
        `~propositions.axiomatic_systems.I0`,
        `~propositions.axiomatic_systems.I1`, and
        `~propositions.axiomatic_systems.D`.
    """        
    assert proof.is_valid()
    assert len(proof.statement.assumptions) > 0
    for rule in proof.rules:
        assert rule == MP or len(rule.assumptions) == 0
    assumption = proof.statement.assumptions[-1]

    new_assumptions = proof.statement.assumptions[:-1]
    
    new_conclusion = Formula('->', assumption, proof.statement.conclusion)
    
    line_map = {}
    new_lines = []

    for i, line in enumerate(proof.lines):
        if line.rule is None:
            if line.formula == assumption:
                new_lines.append(Proof.Line(
                    Formula('->', assumption, assumption),
                    I0,
                    []
                ))
            else:
                new_lines.append(Proof.Line(line.formula))
                new_lines.append(Proof.Line(
                    Formula('->', line.formula,
                           Formula('->', assumption, line.formula)),
                    I1,
                    []
                ))
                new_lines.append(Proof.Line(
                    Formula('->', assumption, line.formula),
                    MP,
                    (len(new_lines)-2, len(new_lines)-1)
                ))
        
        elif line.rule != MP:
            
            new_lines.append(Proof.Line(line.formula, line.rule, []))
            new_lines.append(Proof.Line(
                Formula('->', line.formula,
                       Formula('->', assumption, line.formula)),
                I1,
                []
            ))
            new_lines.append(Proof.Line(
                Formula('->', assumption, line.formula),
                MP,
                (len(new_lines)-2, len(new_lines)-1)
            ))
        
        else:
            assert line.rule == MP
            j, k = line.assumptions
            A = proof.lines[j].formula
            F = line.formula
            d_instance = Formula('->',
                Formula('->', assumption, Formula('->', A, F)),
                Formula('->',
                    Formula('->', assumption, A),
                    Formula('->', assumption, F)
                )
            )

            new_lines.append(Proof.Line(d_instance, D, []))
            new_lines.append(Proof.Line(
                Formula('->',
                    Formula('->', assumption, A),
                    Formula('->', assumption, F)
                ),
                MP,
                (line_map[k], len(new_lines)-1)
            ))
            new_lines.append(Proof.Line(
                Formula('->', assumption, F),
                MP,
                (line_map[j], len(new_lines)-1)
            ))
    
        line_map[i] = len(new_lines) - 1
    assert new_lines[-1].formula == new_conclusion

    new_rules = proof.rules.union({MP, I0, I1, D})
    new_statement = InferenceRule(new_assumptions, new_conclusion)
    
    return Proof(new_statement, new_rules, new_lines)

def prove_from_opposites(proof_of_affirmation: Proof,
                         proof_of_negation: Proof,
                         conclusion: Formula) -> Proof:

    affirmation = proof_of_affirmation.statement.conclusion

    new_lines = []
    for line in proof_of_affirmation.lines:
        new_lines.append(line)

    affirmation_line = len(new_lines) - 1
    offset = len(new_lines)
    for line in proof_of_negation.lines:
        if line.rule is None:
            new_lines.append(line)
        else:
            new_lines.append(
                Proof.Line(
                    line.formula,
                    line.rule,
                    tuple(i + offset for i in line.assumptions)
                )
            )

    negation_line = len(new_lines) - 1
    i2_instance = Formula(
        '->',
        Formula('~', affirmation),
        Formula('->', affirmation, conclusion)
    )

    new_lines.append(Proof.Line(i2_instance, I2, []))
    i2_line = len(new_lines) - 1
    new_lines.append(
        Proof.Line(
            Formula('->', affirmation, conclusion),
            MP,
            (negation_line, i2_line)
        )
    )
    mp1_line = len(new_lines) - 1
    new_lines.append(
        Proof.Line(
            conclusion,
            MP,
            (affirmation_line, mp1_line)
        )
    )

    new_rules = proof_of_affirmation.rules.union({I2})
    new_statement = InferenceRule(
        proof_of_affirmation.statement.assumptions,
        conclusion
    )

    return Proof(new_statement, new_rules, new_lines)

    
def prove_by_way_of_contradiction(proof: Proof) -> Proof:

    not_formula = proof.statement.assumptions[-1]
    formula = not_formula.first
    implication_proof = remove_assumption(proof)

    new_lines = list(implication_proof.lines)

    implication_line = len(new_lines) - 1

    p = Formula.parse('p')
    p_implies_p = Formula('->', p, p)
    n_instance = Formula(
        '->',
        Formula('->',
                Formula('~', formula),
                Formula('~', p_implies_p)),
        Formula('->',
                p_implies_p,
                formula)
    )

    new_lines.append(Proof.Line(n_instance, N, []))
    n_line = len(new_lines) - 1
    new_lines.append(
        Proof.Line(
            Formula('->', p_implies_p, formula),
            MP,
            (implication_line, n_line)
        )
    )
    mp1_line = len(new_lines) - 1
    new_lines.append(Proof.Line(p_implies_p, I0, []))
    pp_line = len(new_lines) - 1
    new_lines.append(
        Proof.Line(
            formula,
            MP,
            (pp_line, mp1_line)
        )
    )

    new_statement = InferenceRule(
        proof.statement.assumptions[:-1],
        formula
    )

    new_rules = proof.rules.union({MP, I0, I1, D, N})

    return Proof(new_statement, new_rules, new_lines)
