# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2025
# File name: propositions/tautology.py

"""The Tautology Theorem and its implications."""

from typing import List, Sequence, Union

from logic_utils import frozendict

from propositions.syntax import *
from propositions.semantics import *
from propositions.proofs import *
from propositions.axiomatic_systems import *
from propositions.deduction import *


def is_model(model: Model) -> bool:
    """Checks if the given object is a valid model.
    
    Parameters:
        model: object to check.
        
    Returns:
        ``True`` if the given object is a valid model, ``False`` otherwise.
    """
    if not isinstance(model, dict):
        return False
    for key, value in model.items():
        if not is_variable(key):
            return False
        if not isinstance(value, bool):
            return False
    return True

def formulas_capturing_model(model: Model) -> List[Formula]:
    """Computes the formulas that capture the given model: ``'``\\ `x`\\ ``'``
    for each variable name `x` that is assigned the value ``True`` in the given
    model, and ``'~``\\ `x`\\ ``'`` for each variable name `x` that is assigned
    the value ``False``.

    Parameters:
        model: model to construct the formulas for.

    Returns:
        A list of the constructed formulas, ordered alphabetically by variable
        name.

    Examples:
        >>> formulas_capturing_model({'p2': False, 'p1': True, 'q': True})
        [p1, ~p2, q]
    """
    assert is_model(model)
    # Task 6.1a
    
    # Получаем отсортированные по алфавиту переменные
    variables = sorted(model.keys())
    
    formulas = []
    for var in variables:
        if model[var]:
            formulas.append(Formula(var))
        else:
            formulas.append(Formula('~', Formula(var)))
    
    return formulas
    # Task 6.1a

def prove_in_model(formula: Formula, model: Model) -> Proof:
    assert formula.operators().issubset({'->', '~'})
    assert is_model(model)

    assumptions = list(formulas_capturing_model(model))
    lines = []

    # добавляем предположения
    for assumption in assumptions:
        lines.append(Proof.Line(assumption))

    def prove(f: Formula) -> int:
        # -------- переменная --------
        if is_variable(f.root):
            for i, assumption in enumerate(assumptions):
                if assumption == f:
                    return i
            raise ValueError("Variable not in assumptions")

        # -------- отрицание --------
        if f.root == '~':
            phi = f.first

            # если формула истинна в модели, доказываем phi
            if evaluate(f, model):
                # тогда phi ложна
                # значит ~phi есть в предположениях
                for i, assumption in enumerate(assumptions):
                    if assumption == f:
                        return i
            else:
                # надо доказать ~~phi
                phi_index = prove(phi)

                implication = Formula('->', phi,
                                      Formula('~', Formula('~', phi)))
                lines.append(Proof.Line(implication, NN, []))

                lines.append(Proof.Line(
                    Formula('~', Formula('~', phi)),
                    MP,
                    (phi_index, len(lines) - 1)
                ))

                return len(lines) - 1

        # -------- импликация --------
        if f.root == '->':
            phi = f.first
            psi = f.second

            if evaluate(f, model):
                # импликация истинна

                if evaluate(psi, model):
                    psi_index = prove(psi)

                    implication = Formula('->', psi,
                                          Formula('->', phi, psi))
                    lines.append(Proof.Line(implication, I1, []))

                    lines.append(Proof.Line(
                        Formula('->', phi, psi),
                        MP,
                        (psi_index, len(lines) - 1)
                    ))

                    return len(lines) - 1

                else:
                    # тогда phi ложна
                    not_phi = Formula('~', phi)
                    not_phi_index = prove(not_phi)

                    implication = Formula('->', not_phi,
                                          Formula('->', phi, psi))
                    lines.append(Proof.Line(implication, I2, []))

                    lines.append(Proof.Line(
                        Formula('->', phi, psi),
                        MP,
                        (not_phi_index, len(lines) - 1)
                    ))

                    return len(lines) - 1

            else:
                # импликация ложна → phi истинна и psi ложна
                phi_index = prove(phi)
                not_psi = Formula('~', psi)
                not_psi_index = prove(not_psi)

                # используем аксиому NI:
                # phi -> (~psi -> ~(phi->psi))
                ni_formula = Formula('->', phi,
                                     Formula('->', not_psi,
                                             Formula('~', f)))
                lines.append(Proof.Line(ni_formula, NI, []))

                lines.append(Proof.Line(
                    Formula('->', not_psi, Formula('~', f)),
                    MP,
                    (phi_index, len(lines) - 1)
                ))

                lines.append(Proof.Line(
                    Formula('~', f),
                    MP,
                    (not_psi_index, len(lines) - 1)
                ))

                return len(lines) - 1

        raise ValueError("Unsupported formula")

    # если формула истинна — доказываем её
    if evaluate(formula, model):
        prove(formula)
        conclusion = formula
    else:
        neg = Formula('~', formula)
        prove(neg)
        conclusion = neg

    statement = InferenceRule(tuple(assumptions), conclusion)
    return Proof(statement, AXIOMATIC_SYSTEM, lines)


def reduce_assumption(proof_from_affirmation: Proof,
                      proof_from_negation: Proof) -> Proof:
    """Combines the two given proofs, both of the same formula `conclusion` and
    from the same assumptions except that the last assumption of the latter is
    the negation of that of the former, into a single proof of `conclusion` from
    only the common assumptions.

    Parameters:
        proof_from_affirmation: valid proof of `conclusion` from one or more
            assumptions, the last of which is an assumption `assumption`.
        proof_from_negation: valid proof of `conclusion` from the same
            assumptions and inference rules of `proof_from_affirmation`, but
            with the last assumption being ``'~``\\ `assumption`\\ ``'`` instead
            of `assumption`.

    Returns:
        A valid proof of `conclusion` from only the assumptions common to the
        given proofs (i.e., without the last assumption of each), via the same
        inference rules of the given proofs and in addition
        `~propositions.axiomatic_systems.MP`,
        `~propositions.axiomatic_systems.I0`,
        `~propositions.axiomatic_systems.I1`,
        `~propositions.axiomatic_systems.D`, and
        `~propositions.axiomatic_systems.R`.

    Examples:
        If `proof_from_affirmation` is of ``['p', '~q', 'r'] ==> '(p&(r|~r))'``,
        then `proof_from_negation` must be of
        ``['p', '~q', '~r'] ==> '(p&(r|~r))'`` and the returned proof is of
        ``['p', '~q'] ==> '(p&(r|~r))'``.
    """
    assert proof_from_affirmation.is_valid()
    assert proof_from_negation.is_valid()
    assert proof_from_affirmation.statement.conclusion == \
           proof_from_negation.statement.conclusion
    assert len(proof_from_affirmation.statement.assumptions) > 0
    assert len(proof_from_negation.statement.assumptions) > 0
    assert proof_from_affirmation.statement.assumptions[:-1] == \
           proof_from_negation.statement.assumptions[:-1]
    assert Formula('~', proof_from_affirmation.statement.assumptions[-1]) == \
           proof_from_negation.statement.assumptions[-1]
    assert proof_from_affirmation.rules == proof_from_negation.rules
    # Task 6.2

def prove_tautology(tautology: Formula, model: Model = frozendict()) -> Proof:
    """Proves the given tautology from the formulas that capture the given
    model.

    Parameters:
        tautology: tautology that contains no constants or operators beyond
            ``'->'`` and ``'~'``, to prove.
        model: model over a (possibly empty) prefix (with respect to the
            alphabetical order) of the variable names of `tautology`, from whose
            formulas to prove.

    Returns:
        A valid proof of the given tautology from the formulas that capture the
        given model, in the order returned by
        `formulas_capturing_model`\\ ``(``\\ `model`\\ ``)``, via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`.

    Examples:
        >>> proof = prove_tautology(Formula.parse('(~(p->p)->q)'),
        ...                         {'p': True, 'q': False})
        >>> proof.is_valid()
        True
        >>> proof.statement.conclusion
        (~(p->p)->q)
        >>> proof.statement.assumptions
        (p, ~q)
        >>> proof.rules == AXIOMATIC_SYSTEM
        True

        >>> proof = prove_tautology(Formula.parse('(~(p->p)->q)'))
        >>> proof.is_valid()
        True
        >>> proof.statement.conclusion
        (~(p->p)->q)
        >>> proof.statement.assumptions
        ()
        >>> proof.rules == AXIOMATIC_SYSTEM
        True
    """
    assert is_tautology(tautology)
    assert tautology.operators().issubset({'->', '~'})
    assert is_model(model)
    assert sorted(tautology.variables())[:len(model)] == sorted(model.keys())
    # Task 6.3a

def proof_or_counterexample(formula: Formula) -> Union[Proof, Model]:
    """Either proves the given formula or finds a model in which it does not
    hold.

    Parameters:
        formula: formula that contains no constants or operators beyond ``'->'``
            and ``'~'``, to either prove or find a counterexample for.

    Returns:
        If the given formula is a tautology, then an assumptionless proof of the
        formula via `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`,
        otherwise a model in which the given formula does not hold.
    """
    assert formula.operators().issubset({'->', '~'})
    # Task 6.3b

def encode_as_formula(rule: InferenceRule) -> Formula:
    """Encodes the given inference rule as a formula consisting of a chain of
    implications.

    Parameters:
        rule: inference rule to encode.

    Returns:
        The formula encoding the given rule.

    Examples:
        >>> encode_as_formula(InferenceRule([Formula('p1'), Formula('p2'),
        ...                                  Formula('p3'), Formula('p4')],
        ...                                 Formula('q')))
        (p1->(p2->(p3->(p4->q))))

        >>> encode_as_formula(InferenceRule([], Formula('q')))
        q
    """
    # Task 6.4a

def prove_sound_inference(rule: InferenceRule) -> Proof:
    """Proves the given sound inference rule.

    Parameters:
        rule: sound inference rule whose assumptions and conclusion contain no
            constants or operators beyond ``'->'`` and ``'~'``, to prove.

    Returns:
        A valid proof of the given sound inference rule via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`.
    """
    assert is_sound_inference(rule)
    for formula in {rule.conclusion}.union(rule.assumptions):
        assert formula.operators().issubset({'->', '~'})
    # Task 6.4b

def model_or_inconsistency(formulas: Sequence[Formula]) -> Union[Model, Proof]:
    """Either finds a model in which all the given formulas hold, or proves
    ``'~(p->p)'`` from these formulas.

    Parameters:
        formulas: formulas that use only the operators ``'->'`` and ``'~'``, to
            either find a model of, or prove ``'~(p->p)'`` from.

    Returns:
        A model in which all of the given formulas hold if such exists,
        otherwise a valid proof of ``'~(p->p)'`` from the given formulas via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`.
    """
    for formula in formulas:
        assert formula.operators().issubset({'->', '~'})
    # Task 6.5

def prove_in_model_full(formula: Formula, model: Model) -> Proof:
    """Either proves the given formula or proves its negation, from the formulas
    that capture the given model.

    Parameters:
        formula: formula that contains no operators beyond ``'->'``, ``'~'``,
            ``'&'``, and ``'|'`` (and may contain constants), whose affirmation
            or negation is to prove.
        model: model from whose formulas to prove.

    Returns:
        If `formula` evaluates to ``True`` in the given model, then a valid
        proof of `formula`; otherwise a valid proof of ``'~``\\ `formula`\\ ``'``.
        The returned proof is from the formulas that capture the given model, in
        the order returned by `formulas_capturing_model`\\ ``(``\\ `model`\\ ``)``,
        via `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM_FULL`.

    Examples:
        >>> proof = prove_in_model_full(Formula.parse('(p&q7)'),
        ...                             {'q7': True, 'p': True})
        >>> proof.is_valid()
        True
        >>> proof.statement.conclusion
        (p&q7)
        >>> proof.statement.assumptions
        (p, q7)
        >>> proof.rules == AXIOMATIC_SYSTEM_FULL
        True

        >>> proof = prove_in_model_full(Formula.parse('(p&q7)'),
        ...                             {'q7': False, 'p': True})
        >>> proof.is_valid()
        True
        >>> proof.statement.conclusion
        ~(p&q7)
        >>> proof.statement.assumptions
        (p, ~q7)
        >>> proof.rules == AXIOMATIC_SYSTEM_FULL
        True
    """
    assert formula.operators().issubset({'T', 'F', '->', '~', '&', '|'})
    assert is_model(model)
    # Optional Task 6.6
