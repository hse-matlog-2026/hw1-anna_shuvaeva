
from __future__ import annotations
from typing import AbstractSet, FrozenSet, List, Mapping, Optional, Sequence, \
                   Set, Tuple, Union

from logic_utils import frozen, memoized_parameterless_method
from propositions.syntax import *
SpecializationMap = Mapping[str, Formula]

@frozen
class InferenceRule:
    assumptions: Tuple[Formula, ...]
    conclusion: Formula

    def __init__(self, assumptions: Sequence[Formula], conclusion: Formula):
        """Initializes an `InferenceRule` from its assumptions and conclusion.

        Parameters:
            assumptions: the assumptions for the rule.
            conclusion: the conclusion for the rule.
        """
        self.assumptions = tuple(assumptions)
        self.conclusion = conclusion

    @memoized_parameterless_method
    def __repr__(self) -> str:
        """Computes a string representation of the current inference rule.

        Returns:
            A string representation of the current inference rule.
        """
        return str([str(assumption) for assumption in self.assumptions]) + \
               ' ==> ' + "'" + str(self.conclusion) + "'"

    def __eq__(self, other: object) -> bool:
        """Compares the current inference rule with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is an `InferenceRule` object that
            equals the current inference rule, ``False`` otherwise.
        """
        return isinstance(other, InferenceRule) and \
               self.assumptions == other.assumptions and \
               self.conclusion == other.conclusion

    def __ne__(self, other: object) -> bool:
        """Compares the current inference rule with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is not an `InferenceRule` object or
            does not does not equal the current inference rule, ``False``
            otherwise.
        """
        return not self == other

    def __hash__(self) -> int:
        return hash(str(self))
        
    def variables(self) -> Set[str]:
        result = set()
        for assumption in self.assumptions:
            result.update(assumption.variables())
        result.update(self.conclusion.variables())
        return result

    def specialize(self, specialization_map: SpecializationMap) -> \
            InferenceRule:
        """Specializes the current inference rule by simultaneously substituting
        each variable name `v` that is a key in `specialization_map` with the
        formula `specialization_map[v]`.

        Parameters:
            specialization_map: mapping defining the specialization to be
                performed.

        Returns:
            The resulting inference rule.
        """        
        for variable in specialization_map:
            assert is_variable(variable)
        # Task 4.4
        specialized_assumptions = []
        for assumption in self.assumptions:
            specialized_assumptions.append(
                assumption.substitute_variables(specialization_map)
            )
        
        specialized_conclusion = self.conclusion.substitute_variables(
            specialization_map
        )
        
        return InferenceRule(specialized_assumptions, specialized_conclusion)

    @staticmethod
    def _merge_specialization_maps(
            specialization_map1: Union[SpecializationMap, None],
            specialization_map2: Union[SpecializationMap, None]) -> \
            Union[SpecializationMap, None]:
        """Merges the given specialization maps.

        Parameters:
            specialization_map1: first map to merge, or ``None``.
            specialization_map2: second map to merge, or ``None``.

        Returns:
            A single map containing all (variable, formula) pairs that appear in
            either of the given maps, or ``None`` if one of the given maps is
            ``None`` or if a variable appears in both given maps but is mapped
            to different formulas.
        """
        # Task 4.5a
        if specialization_map1 is None or specialization_map2 is None:
            return None
        
        result = dict(specialization_map1)
        
        for var, formula in specialization_map2.items():
            if var in result:
                if result[var] != formula:
                    return None
            else:
                result[var] = formula
        
        return result
        
    @staticmethod
    def _formula_specialization_map(general: Formula,
                                    special: Formula) -> \
            Union[SpecializationMap, None]:
        """Computes the minimal specialization map by which the given general
        formula becomes the given special formula.

        Parameters:
            general: general formula.
            special: special formula.

        Returns:
            The computed specialization map, or ``None`` if `special` is in fact
            not a specialization of `general`.
        """
        if is_variable(general.root):
            return {general.root: special}
        
        if general.root != special.root:
            return None
        
        if is_constant(general.root):
            if general.root == special.root:
                return {}
            else:
                return None
    
        if is_unary(general.root):
            return InferenceRule._formula_specialization_map(
                general.first, special.first
            )
        left_map = InferenceRule._formula_specialization_map(
            general.first, special.first
        )
        if left_map is None:
            return None
        
        right_map = InferenceRule._formula_specialization_map(
            general.second, special.second
        )
        if right_map is None:
            return None
        
        return InferenceRule._merge_specialization_maps(left_map, right_map)

    def specialization_map(self, specialization: InferenceRule) -> \
            Union[SpecializationMap, None]:
        if len(self.assumptions) != len(specialization.assumptions):
            return None
        
        total_map = {}
        
        for gen_assump, spec_assump in zip(self.assumptions, specialization.assumptions):
            assump_map = InferenceRule._formula_specialization_map(
                gen_assump, spec_assump
            )
            if assump_map is None:
                return None
            
            total_map = InferenceRule._merge_specialization_maps(
                total_map, assump_map
            )
            if total_map is None:
                return None
        
        conclusion_map = InferenceRule._formula_specialization_map(
            self.conclusion, specialization.conclusion
        )
        if conclusion_map is None:
            return None
    
        return InferenceRule._merge_specialization_maps(
            total_map, conclusion_map
        )

    def is_specialization_of(self, general: InferenceRule) -> bool:
        """Checks if the current inference rule is a specialization of the given
        inference rule.

        Parameters:
            general: non-specialized inference rule to check.

        Returns:
            ``True`` if the current inference rule is a specialization of
            `general`, ``False`` otherwise.
        """
        return general.specialization_map(self) is not None

@frozen
class Proof:
    """An immutable deductive proof in Propositional Logic, comprised of a
    statement in the form of an inference rule, a set of inference rules that
    may be used in the proof, and a list of lines that prove the statement via
    these inference rules.

    Attributes:
        statement (`InferenceRule`): the statement proven by the proof.
        rules (`~typing.AbstractSet`\\[`InferenceRule`]): the allowed rules of
            the proof.
        lines (`~typing.Tuple`\\[`Line`]): the lines of the proof.
    """
    statement: InferenceRule
    rules: FrozenSet[InferenceRule]
    lines: Tuple[Proof.Line, ...]
    
    def __init__(self, statement: InferenceRule,
                 rules: AbstractSet[InferenceRule],
                 lines: Sequence[Proof.Line]):
        """Initializes a `Proof` from its statement, allowed inference rules,
        and lines.

        Parameters:
            statement: the statement to be proven by the proof.
            rules: the allowed rules for the proof.
            lines: the lines for the proof.
        """
        self.statement = statement
        self.rules = frozenset(rules)
        self.lines = tuple(lines)

    @frozen
    class Line:
        """An immutable line in a deductive proof, comprised of a formula that
        is justified either as an assumption of the proof, or as the conclusion
        of a specialization of an allowed inference rule of the proof, the
        assumptions of which are justified by previous lines in the proof.

        Attributes:
            formula (`~propositions.syntax.Formula`): the formula justified by
                the line.
            rule (`~typing.Optional`\\[`InferenceRule`]): the inference rule,
                out of those allowed in the proof, that has a specialization
                that concludes the formula; or ``None`` if the formula is
                justified as an assumption of the proof.
            assumptions (`~typing.Optional`\\[`~typing.Tuple`\\[`int`]): tuple
                of zero or more numbers of previous lines in the proof whose
                formulas are the respective assumptions of the specialization of
                the rule that concludes the formula, if the formula is not
                justified as an assumption of the proof.
        """
        formula: Formula
        rule: Optional[InferenceRule]
        assumptions: Optional[Tuple[int, ...]]

        def __init__(self, formula: Formula,
                     rule: Optional[InferenceRule] = None,
                     assumptions: Optional[Sequence[int]] = None):
            """Initializes a `~Proof.Line` from its formula, and optionally its
            rule and numbers of justifying previous lines.

            Parameters:
                formula: the formula to be justified by the line.
                rule: the inference rule, out of those allowed in the proof,
                    that has a specialization that concludes the formula; or
                    ``None`` if the formula is to be justified as an assumption
                    of the proof.
                assumptions: numbers of previous lines in the proof whose
                    formulas are the respective assumptions of the
                    specialization of the rule that concludes the formula, or
                    ``None`` if the formula is to be justified as an assumption
                    of the proof.
            """
            assert (rule is None and assumptions is None) or \
                   (rule is not None and assumptions is not None)
            self.formula = formula
            self.rule = rule
            if assumptions is not None:
                self.assumptions = tuple(assumptions)

        def __repr__(self) -> str:
            """Computes a string representation of the current line.

            Returns:
                A string representation of the current line.
            """
            if self.rule is None:
                return str(self.formula)
            else:
                r = str(self.formula) + '    (Inference Rule ' + str(self.rule)
                if len(self.assumptions) == 1:
                    r += ' on line ' + str(self.assumptions[0])
                elif len(self.assumptions) > 1:
                    r += ' on lines ' + ','.join(map(str, self.assumptions))
                r += ')'
                return r

        def is_assumption(self) -> bool:
            """Checks if the current proof line is justified as an assumption of
            the proof.

            Returns:
                ``True`` if the current proof line is justified as an assumption
                of the proof, ``False`` otherwise.
            """
            return self.rule is None
        
    def __repr__(self) -> str:
        """Computes a string representation of the current proof.

        Returns:
            A string representation of the current proof.
        """
        r = 'Proof of ' + str(self.statement) + ' via inference rules:\n'
        for rule in self.rules:
            r += '  ' + str(rule) + '\n'
        r += 'Lines:\n'
        for i in range(len(self.lines)):
            r += ('%3d) ' % i) + str(self.lines[i]) + '\n'
        r += "QED\n"
        return r

    def rule_for_line(self, line_number: int) -> Union[InferenceRule, None]:
    
        line = self.lines[line_number]
        if line.rule is None:
            return None
        
        assumption_formulas = []
        for assumption_line_num in line.assumptions:
            assumption_formulas.append(self.lines[assumption_line_num].formula)
        
        return InferenceRule(assumption_formulas, line.formula)

    def is_line_valid(self, line_number: int) -> bool:

        line = self.lines[line_number]
        if line.rule is None:
            return line.formula in self.statement.assumptions
        for assumption_line in line.assumptions:
            if assumption_line >= line_number:
                return False
        inferred_rule = self.rule_for_line(line_number)
        if inferred_rule is None:
            return False
        
        if not inferred_rule.is_specialization_of(line.rule):
            return False
    
        rule_allowed = False
        for allowed_rule in self.rules:
            if line.rule == allowed_rule or line.rule.is_specialization_of(allowed_rule):
                rule_allowed = True
                break
        
        return rule_allowed

    def is_valid(self) -> bool:
        if len(self.lines) == 0:
            return False
        if self.lines[-1].formula != self.statement.conclusion:
            return False
    
        valid_lines = [False] * len(self.lines)
        
        for i in range(len(self.lines)):
            line = self.lines[i]
            
            if line.rule is None:
                valid_lines[i] = (line.formula in self.statement.assumptions)
            else:
                for assumption in line.assumptions:
                    if assumption >= i:
                        return False
                    if not valid_lines[assumption]: 
                        return False
            
                if not self.is_line_valid(i):
                    return False
                
                valid_lines[i] = True
        
        return all(valid_lines)

def prove_specialization(proof: Proof, specialization: InferenceRule) -> Proof:
    assert proof.is_valid()
    assert specialization.is_specialization_of(proof.statement)
    specialization_map = proof.statement.specialization_map(specialization)
    new_lines = []
    for line in proof.lines:
    
        new_formula = line.formula.substitute_variables(specialization_map)
        
        if line.rule is None:
        
            new_lines.append(Proof.Line(new_formula))
        else:
            new_lines.append(Proof.Line(
                new_formula,
                line.rule,
                line.assumptions
            ))
    
    return Proof(specialization, proof.rules, new_lines)

def _inline_proof_once(main_proof: Proof, line_number: int,
                       lemma_proof: Proof) -> Proof:
    
    assert main_proof.is_valid()
    assert line_number < len(main_proof.lines)
    assert main_proof.lines[line_number].rule == lemma_proof.statement
    assert lemma_proof.is_valid()
    
    
    line_to_replace = main_proof.lines[line_number]
    actual_rule = main_proof.rule_for_line(line_number)
    if actual_rule is None:
        raise ValueError(f"Line {line_number} is not a rule application")
    specialized_lemma_proof = prove_specialization(lemma_proof, actual_rule)
    
    new_lines = []
    new_lines.extend(main_proof.lines[:line_number])
    lemma_to_main_map = {}
    lemma_assumptions = []
    for i, line in enumerate(specialized_lemma_proof.lines):
        if line.rule is None:
            lemma_assumptions.append(i)
    
    for lemma_idx in lemma_assumptions:
        lemma_formula = specialized_lemma_proof.lines[lemma_idx].formula
        found = False
    
        for main_idx in line_to_replace.assumptions:
            if main_proof.lines[main_idx].formula == lemma_formula:
                lemma_to_main_map[lemma_idx] = main_idx
                found = True
                break
        
        if not found:
            for i in range(line_number):
                if main_proof.lines[i].formula == lemma_formula:
                    lemma_to_main_map[lemma_idx] = i
                    found = True
                    break
    
    
    lemma_rule_lines_added = 0
    
    for i, lemma_line in enumerate(specialized_lemma_proof.lines):
        if lemma_line.rule is not None:
            
            new_assumptions = []
            for a in lemma_line.assumptions:
                if a in lemma_to_main_map:
                    new_assumptions.append(lemma_to_main_map[a])
                else:
                    rule_lines_before = 0
                    for k in range(a):
                        if specialized_lemma_proof.lines[k].rule is not None:
                            rule_lines_before += 1
                    
                    position = line_number + rule_lines_before
                    new_assumptions.append(position)
            
            new_lines.append(Proof.Line(
                lemma_line.formula,
                lemma_line.rule,
                tuple(new_assumptions)
            ))
            
            lemma_to_main_map[i] = len(new_lines) - 1
            lemma_rule_lines_added += 1
    

    offset = lemma_rule_lines_added - 1
    
    for i in range(line_number + 1, len(main_proof.lines)):
        old_line = main_proof.lines[i]
        if old_line.rule is None:
            new_lines.append(old_line)
        else:
            new_assumptions = []
            for a in old_line.assumptions:
                if a == line_number:
                    new_assumptions.append(line_number + lemma_rule_lines_added - 1)
                elif a > line_number:
                    new_assumptions.append(a + offset)
                else:
                    new_assumptions.append(a)
            
            new_lines.append(Proof.Line(
                old_line.formula,
                old_line.rule,
                tuple(new_assumptions)
            ))

    new_rules = main_proof.rules.union(lemma_proof.rules)
    
    return Proof(main_proof.statement, new_rules, new_lines)
    
def inline_proof(main_proof: Proof, lemma_proof: Proof) -> Proof:
    assert main_proof.is_valid()
    assert lemma_proof.is_valid()
    proof = main_proof
    lines_with_lemma = []
    for i, line in enumerate(proof.lines):
        if line.rule == lemma_proof.statement:
            lines_with_lemma.append(i)
    
    lines_with_lemma.sort(reverse=True)
    
    for line_number in lines_with_lemma:
        proof = _inline_proof_once(proof, line_number, lemma_proof)
    new_rules = proof.rules.union(lemma_proof.rules) - {lemma_proof.statement}
    
    return Proof(proof.statement, new_rules, proof.lines)