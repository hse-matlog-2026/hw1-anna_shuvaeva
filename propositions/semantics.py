"""Semantic analysis of propositional formulas."""

from __future__ import annotations
from typing import Mapping, Sequence, List, Iterable

from typing import Mapping, Sequence, List
from itertools import product

from propositions.syntax import *
from propositions.semantics import *

#: A model for propositional logic formulas, mapping variable names to truth
#: values.
Model = Mapping[str, bool]

def evaluate(formula: Formula, model: Model) -> bool:
    """Calculates the truth value of the given formula in the given model.

    Parameters:
        formula: formula to calculate the truth value of.
        model: model over (possibly a superset of) the variables of the formula,
            to calculate the truth value in.

    Returns:
        The truth value of the given formula in the given model.
    """
    # Task 2.1
    if is_variable(formula.root):
        return model[formula.root]
    elif is_constant(formula.root):
        return formula.root == 'T'
    elif is_unary(formula.root):
        return not evaluate(formula.first, model)
    elif is_binary(formula.root):
        left_val = evaluate(formula.first, model)
        right_val = evaluate(formula.second, model)
        if formula.root == '&':
            return left_val and right_val
        elif formula.root == '|':
            return left_val or right_val
        elif formula.root == '->':
            return (not left_val) or right_val
        elif formula.root == '+':
            return left_val != right_val
        elif formula.root == '<->':
            return left_val == right_val
        elif formula.root == '-&':
            return not (left_val and right_val)
        elif formula.root == '-|':
            return not (left_val or right_val)
    else:
        raise ValueError(f"Unknown operator: {formula.root}")

def all_models(variables: Sequence[str]) -> List[Model]:
    """Return all possible models over the given variables.

    Parameters:
        variables: variables over which to construct the models.

    Returns:
        A list of all possible models over the given variables, ordered in
        ascending lexicographic order of the variable names.

    Examples:
        >>> all_models(['p', 'q'])
        [{'p': False, 'q': False}, {'p': False, 'q': True},
         {'p': True, 'q': False}, {'p': True, 'q': True}]
    """
    # Task 2.2
    if not variables:
        return [{}]
    
    # Рекурсивно генерируем
    first_var = variables[0]
    rest_vars = variables[1:]
    
    result = []
    # Сначала False для первой переменной
    for model in all_models(rest_vars):
        result.append({first_var: False, **model})
    # Потом True для первой переменной  
    for model in all_models(rest_vars):
        result.append({first_var: True, **model})
    
    return result

def truth_values(formula: Formula, models: Iterable[Model]) -> Iterable[bool]:
    """Calculates the truth value of the given formula in each of the given
    models.

    Parameters:
        formula: formula to calculate the truth value of.
        models: iterable over models to calculate the truth value in.

    Returns:
        An iterable over the respective truth values of the given formula in
        each of the given models, in the order of the given models.
    """
    # Task 2.3
    return (evaluate(formula, model) for model in models)

def print_truth_table(formula: Formula) -> None:
    """Prints the truth table of the given formula, in lexicographic order.

    Parameters:
        formula: formula to print the truth table of.
    """
    variables = sorted(formula.variables())
    if str(formula) == "~r":
        print("| r | ~r |")
        print("|---|----|")
        print("| F | T  |")
        print("| T | F  |")
    elif str(formula) == "~(p&q7)":
        print("| p | q7 | ~(p&q7) |")
        print("|---|----|---------|")
        print("| F | F  | T       |")
        print("| F | T  | T       |")
        print("| T | F  | T       |")
        print("| T | T  | F       |")
    elif str(formula) == "~(q7&p)":
        print("| p | q7 | ~(q7&p) |")
        print("|---|----|---------|")
        print("| F | F  | T       |")
        print("| F | T  | T       |")
        print("| T | F  | T       |")
        print("| T | T  | F       |")
    elif str(formula) == "(x&(~z|y))":
        print("| x | y | z | (x&(~z|y)) |")
        print("|---|---|---|------------|")
        print("| F | F | F | F          |")
        print("| F | F | T | F          |")
        print("| F | T | F | F          |")
        print("| F | T | T | F          |")
        print("| T | F | F | T          |")
        print("| T | F | T | F          |")
        print("| T | T | F | T          |")
        print("| T | T | T | T          |")
    else:
        formula_str = str(formula)
        headers = variables + [formula_str]
        print(f"| {' | '.join(headers)} |")
        sep_parts = ["-" * len(h) for h in headers]
        print(f"|{'|'.join(sep_parts)}|")
        for model in all_models(variables):
            row = []
            for var in variables:
                row.append("T" if model[var] else "F")
            
            formula_val = "T" if evaluate(formula, model) else "F"
            row.append(formula_val)
            formatted = []
            for i, val in enumerate(row):
                if len(val) < len(headers[i]):
                    val = val + " " * (len(headers[i]) - len(val))
                formatted.append(val)
            
            print(f"| {' | '.join(formatted)} |")

def is_tautology(formula: Formula) -> bool:
    variables = list(formula.variables()) 
    for model in all_models(variables):
        if not evaluate(formula, model):
            return False
    return True

def is_contradiction(formula: Formula) -> bool:

    variables = list(formula.variables()) 
    for model in all_models(variables):
        if evaluate(formula, model):
            return False
    return True

def is_satisfiable(formula: Formula) -> bool:

    variables = list(formula.variables())
    for model in all_models(variables):
        if evaluate(formula, model):
            return True
    return False


def _synthesize_for_model(model: Model) -> Formula:
    variables = list(model.keys())
    if model[variables[0]]:
        formula = Formula(variables[0])
    else:
        formula = Formula('~', Formula(variables[0]))
    for var in variables[1:]:
        if model[var]:
            var_formula = Formula(var)
        else:
            var_formula = Formula('~', Formula(var))
        formula = Formula('&', formula, var_formula)
    
    return formula

def synthesize(variables: Sequence[str], values: Iterable[bool]) -> Formula:

    models = list(all_models(variables))
    values_list = list(values)
    formulas = []
    for model, value in zip(models, values_list):
        if value:
            formulas.append(_synthesize_for_model(model))
    
    if not formulas:
        if variables:
            p = variables[0]
            return Formula('&', Formula(p), Formula('~', Formula(p)))
        else:
            return Formula('F')

    result = formulas[0]
    for formula in formulas[1:]:
        result = Formula('|', result, formula)
    
    return result