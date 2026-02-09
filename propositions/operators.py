from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:

    if is_variable(formula.root):
        return Formula(formula.root)
    elif is_constant(formula.root):
        if formula.root == 'T':
            return Formula.parse('(z1|~z1)')
        else:  # 'F'
            return Formula.parse('(z1&~z1)')
    elif is_unary(formula.root):
        inner = to_not_and_or(formula.first)
        return Formula('~', inner)
    else:
        left = to_not_and_or(formula.first)
        right = to_not_and_or(formula.second)
        
        if formula.root == '&':
            return Formula('&', left, right)
        elif formula.root == '|':
            return Formula('|', left, right)
        elif formula.root == '->':
            return Formula.parse(f'(~{left}|{right})')
        elif formula.root == '+':
            return Formula.parse(f'(({left}&~{right})|(~{left}&{right}))')
        elif formula.root == '<->':
            return Formula.parse(f'(({left}&{right})|(~{left}&~{right}))')
        elif formula.root == '-&':
            return Formula.parse(f'~({left}&{right})')
        elif formula.root == '-|':
            return Formula.parse(f'~({left}|{right})')

def _eliminate_or(formula: Formula) -> Formula:

    if is_variable(formula.root):
        return formula
    elif is_constant(formula.root):
        return formula
    elif is_unary(formula.root):
        return Formula('~', _eliminate_or(formula.first))
    else:
        left = _eliminate_or(formula.first)
        right = _eliminate_or(formula.second)
        
        if formula.root == '&':
            return Formula('&', left, right)
        elif formula.root == '|':
            return Formula('~', Formula('&', 
                                       Formula('~', left), 
                                       Formula('~', right)))
        else:
            return formula

def to_not_and(formula: Formula) -> Formula:
    f1 = to_not_and_or(formula)
    return _eliminate_or(f1)

def to_nand(formula: Formula) -> Formula:

    f_not_and = to_not_and(formula)
    return _to_nand_from_not_and(f_not_and)

def _to_nand_from_not_and(formula: Formula) -> Formula:

    if is_variable(formula.root):
        return formula
    elif is_unary(formula.root):
        inner = _to_nand_from_not_and(formula.first)
        return Formula('-&', inner, inner)
    else:
        left = _to_nand_from_not_and(formula.first)
        right = _to_nand_from_not_and(formula.second)
        nand = Formula('-&', left, right)
        return Formula('-&', nand, nand)

def to_implies_not(formula: Formula) -> Formula:
    f_not_and = to_not_and(formula)
    return _to_implies_not_from_not_and(f_not_and)

def _to_implies_not_from_not_and(formula: Formula) -> Formula:
    if is_variable(formula.root):
        return formula
    elif is_unary(formula.root):
        return Formula('~', _to_implies_not_from_not_and(formula.first))
    else:
        left = _to_implies_not_from_not_and(formula.first)
        right = _to_implies_not_from_not_and(formula.second)
        return Formula('~', Formula('->', left, Formula('~', right)))

def to_implies_false(formula: Formula) -> Formula:
    f_implies_not = to_implies_not(formula)
    return _to_implies_false_from_implies_not(f_implies_not)

def _to_implies_false_from_implies_not(formula: Formula) -> Formula:
    if is_variable(formula.root):
        return formula
    elif is_unary(formula.root):
        inner = _to_implies_false_from_implies_not(formula.first)
        return Formula('->', inner, Formula('F'))
    else:
        left = _to_implies_false_from_implies_not(formula.first)
        right = _to_implies_false_from_implies_not(formula.second)
        return Formula('->', left, right)