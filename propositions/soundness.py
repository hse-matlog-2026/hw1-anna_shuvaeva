# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/soundness.py

"""Programmatic proof of the soundness of Propositional Logic."""

from typing import Tuple

from propositions.syntax import *
from propositions.semantics import *
from propositions.proofs import *

def rule_nonsoundness_from_specialization_nonsoundness(
        general: InferenceRule, specialization: InferenceRule, model: Model) \
        -> Model:
    """Demonstrates the non-soundness of the given general inference rule given
    an example of the non-soundness of the given specialization of this rule.

    Parameters:
        general: inference rule to the soundness of which to find a
            counterexample.
        specialization: non-sound specialization of `general`.
        model: model in which `specialization` does not hold.

    Returns:
        A model in which `general` does not hold.
    """
    assert specialization.is_specialization_of(general)
    assert not evaluate_inference(specialization, model)
    # Task 4.9
    
    # Get the specialization map
    substitution = general.specialization_map(specialization)
    
    # Build a model for the general rule
    general_model = {}
    
    for var in general.variables():
        if var in substitution:
            # var maps to some formula in specialization
            formula = substitution[var]
            value = evaluate(formula, model)
            general_model[var] = value
        else:
            # Variable doesn't appear in substitution
            general_model[var] = False
    
    return general_model

def nonsound_rule_of_nonsound_proof(proof: Proof, model: Model) -> \
        Tuple[InferenceRule, Model]:
    """Finds a non-sound inference rule used by the given valid proof of a
    non-sound inference rule, and demonstrates the non-soundness of the former
    rule.

    Parameters:
        proof: valid proof of a non-sound inference rule.
        model: model in which the inference rule proved by the given proof does
            not hold.

    Returns:
        A pair of a non-sound inference rule used in the given proof and a model
        in which this rule does not hold.
    """
    assert proof.is_valid()
    assert not evaluate_inference(proof.statement, model)
    # Task 4.10
    
    # Check each line in the proof
    for i in range(len(proof.lines)):
        line = proof.lines[i]
        
        # Skip assumption lines (they don't use inference rules)
        if line.rule is None:
            continue
        
        # Get the actual inference rule applied in this line
        inferred_rule = proof.rule_for_line(i)
        
        # Check if this rule is sound
        if not evaluate_inference(inferred_rule, model):
            # Found a non-sound rule!
            # But we need to return the general rule from proof.rules,
            # not the specific inferred_rule
            
            # Find which general rule from proof.rules was used
            for general_rule in proof.rules:
                # Check if inferred_rule is a specialization of general_rule
                if inferred_rule.is_specialization_of(general_rule):
                    # We already have model where inferred_rule fails
                    # Get a model where general_rule fails
                    general_model = rule_nonsoundness_from_specialization_nonsoundness(
                        general_rule, inferred_rule, model
                    )
                    return (general_rule, general_model)
    
    # If we get here, something is wrong
    raise ValueError("Could not find non-sound rule in proof")
