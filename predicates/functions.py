"""Syntactic conversion of predicate-logic formulas to not use functions and
equality."""

from typing import AbstractSet, List, Set, Union

from logic_utils import fresh_variable_name_generator, is_z_and_number

from predicates.syntax import *
from predicates.semantics import *

def function_name_to_relation_name(function: str) -> str:
    """Converts the given function name to a canonically corresponding relation
    name.

    Parameters:
        function: function name to convert.

    Returns:
        A relation name that is the same as the given function name, except that
        its first letter is capitalized.
    """
    assert is_function(function)
    return function[0].upper() + function[1:]

def relation_name_to_function_name(relation: str) -> str:
    """Converts the given relation name to a canonically corresponding function
    name.

    Parameters:
        relation: relation name to convert.

    Returns:
        A function name `function` such that
        `function_name_to_relation_name`\\ ``(``\\ `function`\\ ``)`` is the given
        relation name.
    """
    assert is_relation(relation)
    return relation[0].lower() + relation[1:]

def replace_functions_with_relations_in_model(model: Model[T]) -> Model[T]:
    """Converts the given model to a canonically corresponding model without any
    function interpretations, replacing each function interpretation with a
    canonically corresponding relation interpretation.

    Parameters:
        model: model to convert, such that there exist no canonically
            corresponding function name and relation name that both have
            interpretations in this model.

    Returns:
        A model obtained from the given model by replacing every function
        interpretation of a function name with a relation interpretation of the
        canonically corresponding relation name, such that the relation
        interpretation contains any tuple
        ``(``\\ `x1`\\ ``,``...\\ ``,``\\ `xn`\\ ``)``  if and only if `x1` is the
        output of the function interpretation for the arguments
        ``(``\\ `x2`\\ ``,``...\\ ``,``\\ `xn`\\ ``)``.
    """
    for function in model.function_interpretations:
        assert function_name_to_relation_name(function) not in \
               model.relation_interpretations

    constant_interpretations = dict(model.constant_interpretations)
    relation_interpretations = dict(model.relation_interpretations)
    for function_name, function_map in model.function_interpretations.items():
        relation_name = function_name_to_relation_name(function_name)
        relation_tuples = set()
        for args, result in function_map.items():
            relation_tuple = (result,) + args
            relation_tuples.add(relation_tuple)
        
        relation_interpretations[relation_name] = relation_tuples
    return Model(
        universe=model.universe,
        constant_interpretations=constant_interpretations,
        relation_interpretations=relation_interpretations,
        function_interpretations={}
    )

def replace_relations_with_functions_in_model(model: Model[T],
                                              original_functions:
                                              AbstractSet[str]) -> \
        Union[Model[T], None]:
    """Converts the given model with no function interpretations to a
    canonically corresponding model with interpretations for the given function
    names, having each new function interpretation replace a canonically
    corresponding relation interpretation.

    Parameters:
        model: model to convert, that contains no function interpretations.
        original_functions: function names for the model to convert to,
            such that no relation name that canonically corresponds to any of
            these function names has an interpretation in the given model.

    Returns:
        A model `model` with the given function names such that
        `replace_functions_with_relations_in_model`\\ ``(``\\ `model`\\ ``)``
        is the given model, or ``None`` if no such model exists.
    """
    assert len(model.function_interpretations) == 0
    for function in original_functions:
        assert is_function(function)
        assert function not in model.function_interpretations
        assert function_name_to_relation_name(function) in \
               model.relation_interpretations
    constant_interpretations = dict(model.constant_interpretations)
    function_interpretations = {}
    relation_interpretations = dict(model.relation_interpretations)
    
    
    for function_name in original_functions:
        relation_name = function_name_to_relation_name(function_name)
        relation_tuples = relation_interpretations[relation_name]

        if not relation_tuples:
            return None
        
        arity = len(next(iter(relation_tuples))) - 1
        function_map = {}

        for tuple_args in relation_tuples:
            result = tuple_args[0]
            args = tuple_args[1:]
            
            if len(args) != arity:
                return None
            
            if result not in model.universe:
                return None
            
            for arg in args:
                if arg not in model.universe:
                    return None
            
            if args in function_map and function_map[args] != result:
                return None
            
            function_map[args] = result

        import itertools
        all_possible_args = itertools.product(model.universe, repeat=arity)
        for args in all_possible_args:
            if args not in function_map:
                return None
    
        function_interpretations[function_name] = function_map
        del relation_interpretations[relation_name]

    return Model(
        universe=model.universe,
        constant_interpretations=constant_interpretations,
        relation_interpretations=relation_interpretations,
        function_interpretations=function_interpretations
    )

def _compile_term(term: Term) -> List[Formula]:
    """Syntactically compiles the given term into a list of single-function
    invocation steps.

    Parameters:
        term: term to compile, whose root is a function invocation, and which
            contains no variable names that are ``z`` followed by a number.

    Returns:
        A list of steps, each of which is a formula of the form
        ``'``\\ `y`\\ ``=``\\ `f`\\ ``(``\\ `x1`\\ ``,``...\\ ``,``\\ `xn`\\ ``)'``,
        where `y` is a new variable name obtained by calling
        `next`\\ ``(``\\ `~logic_utils.fresh_variable_name_generator`\\ ``)``, `f`
        is a function name, and each of the `x`\\ `i` is either a constant name
        or a variable name. If `x`\\ `i` is a new variable name, then it is also
        the left-hand side of a previous step, where all of the steps "leading
        up to" `x1` precede those "leading up" to `x2`, etc. If all the returned
        steps hold in any model, then the left-hand-side variable name of the
        last returned step evaluates in that model to the value of the given
        term.
    """
    assert is_function(term.root)
    for variable in term.variables():
        assert not is_z_and_number(variable)
    
    from logic_utils import fresh_variable_name_generator
    
    steps = []
    arg_vars = []

    for arg in term.arguments:
        if is_function(arg.root):
            arg_steps = _compile_term(arg)
            steps.extend(arg_steps)
            last_step = arg_steps[-1]
            arg_var = last_step.arguments[0].root
            arg_vars.append(arg_var)
        else:
            arg_vars.append(arg.root)

    result_var = next(fresh_variable_name_generator)
    equality = Formula('=', 
                      [Term(result_var), 
                       Term(term.root, [Term(v) for v in arg_vars])])
    steps.append(equality)
    
    return steps

def replace_functions_with_relations_in_formula(formula: Formula) -> Formula:
    """Syntactically converts the given formula to a formula that does not
    contain any function invocations, and is "one-way equivalent" in the sense
    that the former holds in a model if and only if the latter holds in the
    canonically corresponding model with no function interpretations.

    Parameters:
        formula: formula to convert, which contains no variable names that are
            ``z`` followed by a number, and such that there exist no canonically
            corresponding function name and relation name that are both invoked
            in this formula.

    Returns:
        A formula such that the given formula holds in any model `model` if and
        only if the returned formula holds in
        `replace_functions_with_relations_in_model`\\ ``(``\\ `model`\\ ``)``.
    """
    assert len({function_name_to_relation_name(function) for
                function, arity in formula.functions()}.intersection(
                    {relation for relation, arity in formula.relations()})) == 0
    for variable in formula.variables():
        assert not is_z_and_number(variable)
    
    from logic_utils import fresh_variable_name_generator
    if is_equality(formula.root):
        left = formula.arguments[0]
        right = formula.arguments[1]
        
        if is_function(left.root):
            steps = _compile_term(left)
            last_step = steps[-1]
            new_var = last_step.arguments[0].root
            
            all_vars = []
            all_relations = []
            
            for step in steps:
                step_func = step.arguments[1]
                step_relation_name = function_name_to_relation_name(step_func.root)
                step_args = [step.arguments[0]] + list(step_func.arguments)
                step_relation = Formula(step_relation_name, step_args)
                
                step_var = step.arguments[0].root
                all_vars.append(step_var)
                all_relations.append(step_relation)
            
            result = Formula('=', [Term(new_var), right])
            for rel in reversed(all_relations):
                result = Formula('&', rel, result)
            
            for var in reversed(all_vars):
                result = Formula('E', var, result)
            
            return result
        elif is_function(right.root):
            steps = _compile_term(right)
            last_step = steps[-1]
            new_var = last_step.arguments[0].root
            all_vars = []
            all_relations = []
            for step in steps:
                step_func = step.arguments[1]
                step_relation_name = function_name_to_relation_name(step_func.root)
                step_args = [step.arguments[0]] + list(step_func.arguments)
                step_relation = Formula(step_relation_name, step_args)
                
                step_var = step.arguments[0].root
                all_vars.append(step_var)
                all_relations.append(step_relation)
            
            result = Formula('=', [left, Term(new_var)])
            
            for rel in reversed(all_relations):
                result = Formula('&', rel, result)
            for var in reversed(all_vars):
                result = Formula('E', var, result)
            
            return result
        else:
            return formula

    elif is_relation(formula.root):
        args = list(formula.arguments)

        function_steps_list = []
        for i, arg in enumerate(args):
            if is_function(arg.root):
                steps = _compile_term(arg)
                function_steps_list.append((i, steps))
        
        if not function_steps_list:
            return formula
        
        all_new_vars = []
        all_step_relations = []
        
        for i, steps in function_steps_list:
            last_step = steps[-1]
            new_var = last_step.arguments[0].root
            step_func = last_step.arguments[1]
            step_relation_name = function_name_to_relation_name(step_func.root)
            step_args = [last_step.arguments[0]] + list(step_func.arguments)
            step_relation = Formula(step_relation_name, step_args)
            
            all_new_vars.append(new_var)
            all_step_relations.append(step_relation)
            for step in steps[:-1]:
                step_func = step.arguments[1]
                step_relation_name = function_name_to_relation_name(step_func.root)
                step_args = [step.arguments[0]] + list(step_func.arguments)
                step_relation = Formula(step_relation_name, step_args)
                
                step_var = step.arguments[0].root
                all_new_vars.append(step_var)
                all_step_relations.append(step_relation)
        
        
        current_args = args[:]
        for i, steps in function_steps_list:
            last_step = steps[-1]
            new_var = last_step.arguments[0].root
            current_args[i] = Term(new_var)
        
        main_formula = Formula(formula.root, current_args)
        result = main_formula
        for step_relation in all_step_relations:
            result = Formula('&', step_relation, result)
        
        for new_var in reversed(all_new_vars):
            result = Formula('E', new_var, result)
        
        return result
    
    elif is_unary(formula.root):
        new_first = replace_functions_with_relations_in_formula(formula.first)
        return Formula(formula.root, new_first)

    elif is_binary(formula.root):
        new_first = replace_functions_with_relations_in_formula(formula.first)
        new_second = replace_functions_with_relations_in_formula(formula.second)
        return Formula(formula.root, new_first, new_second)
    
    else:
        new_statement = replace_functions_with_relations_in_formula(formula.statement)
        return Formula(formula.root, formula.variable, new_statement)

def replace_functions_with_relations_in_formulas(formulas:
                                                 AbstractSet[Formula]) -> \
        Set[Formula]:
    """Syntactically converts the given set of formulas to a set of formulas
    that do not contain any function invocations, and is "two-way
    equivalent" in the sense that:

    1. The former holds in a model if and only if the latter holds in the
       canonically corresponding model with no function interpretations.
    2. The latter holds in a model if and only if that model has a
       canonically corresponding model with interpretations for the functions
       names of the former, and the former holds in that model.

    Parameters:
        formulas: formulas to convert, which contain no variable names that are
            ``z`` followed by a number, and such that there exist no canonically
            corresponding function name and relation name that are both invoked
            in these formulas.

    Returns:
        A set of formulas, one for each given formula as well as one additional
        formula for each relation name that replaces a function name from the
            given formulas, such that:

        1. The given formulas hold in a model `model` if and only if the
           returned formulas hold in
           `replace_functions_with_relations_in_model`\\ ``(``\\ `model`\\ ``)``.
        2. The returned formulas hold in a model `model` if and only if
           `replace_relations_with_functions_in_model`\\ ``(``\\ `model`\\ ``,``\\ `original_functions`\\ ``)``,
           where `original_functions` are all the function names in the given
           formulas, is a model and the given formulas hold in it.
    """
    assert len(set.union(*[{function_name_to_relation_name(function) for
                            function, arity in formula.functions()}
                           for formula in formulas]).intersection(
                               set.union(*[{relation for relation, arity in
                                            formula.relations()} for
                                           formula in formulas]))) == 0
    for formula in formulas:
        for variable in formula.variables():
            assert not is_z_and_number(variable)
    
    from logic_utils import fresh_variable_name_generator
    
    result = set()
    for formula in formulas:
        compiled = replace_functions_with_relations_in_formula(formula)
        result.add(compiled)
    all_functions = set()
    for formula in formulas:
        for function_name, arity in formula.functions():
            all_functions.add((function_name, arity))
    
    for function_name, arity in all_functions:
        relation_name = function_name_to_relation_name(function_name)

        arg_vars = []
        for i in range(arity):
            var = next(fresh_variable_name_generator)
            arg_vars.append(var)
        
        z = next(fresh_variable_name_generator)
        relation_args = [Term(z)] + [Term(var) for var in arg_vars]
        relation_formula = Formula(relation_name, relation_args)
        exists = Formula('E', z, relation_formula)
        z1 = next(fresh_variable_name_generator)
        z2 = next(fresh_variable_name_generator)
        
        args1 = [Term(z1)] + [Term(var) for var in arg_vars]
        args2 = [Term(z2)] + [Term(var) for var in arg_vars]
        
        r1 = Formula(relation_name, args1)
        r2 = Formula(relation_name, args2)
        equality = Formula('=', [Term(z1), Term(z2)])
        implication = Formula('->', Formula('&', r1, r2), equality)
        forall_z2 = Formula('A', z2, implication)
        forall_z1 = Formula('A', z1, forall_z2)
        
        unique_exists = Formula('&', exists, forall_z1)
        formula_func = unique_exists
        for var in reversed(arg_vars):
            formula_func = Formula('A', var, formula_func)
        
        result.add(formula_func)
    
    return result

def replace_equality_with_SAME_in_formulas(formulas: AbstractSet[Formula]) -> \
        Set[Formula]:
    """Syntactically converts the given set of formulas to a canonically
    corresponding set of formulas that do not contain any equalities, consisting
    of the following formulas:

    1. A formula for each of the given formulas, where each equality is
       replaced with a matching invocation of the relation name ``'SAME'``.
    2. Formula(s) that ensure that in any model of the returned formulas, the
       interpretation of the relation name ``'SAME'`` is reflexive,
       symmetric, and transitive.
    3. For each relation name from the given formulas, formula(s) that ensure
       that in any model of the returned formulas, the interpretation of this
       relation name respects the interpretation of the relation name
       ``'SAME'``.

    Parameters:
        formulas: formulas to convert, that contain no function names and do not
            contain the relation name ``'SAME'``.

    Returns:
        The converted set of formulas.
    """
    for formula in formulas:
        assert len(formula.functions()) == 0
        assert 'SAME' not in \
               {relation for relation, arity in formula.relations()}
    
    from logic_utils import fresh_variable_name_generator
    result = set()
    def replace_equalities_in_formula(f: Formula) -> Formula:
        if is_equality(f.root):
            return Formula('SAME', [f.arguments[0], f.arguments[1]])
        elif is_relation(f.root):
            return Formula(f.root, f.arguments)
        elif is_unary(f.root):
            return Formula(f.root, replace_equalities_in_formula(f.first))
        elif is_binary(f.root):
            return Formula(f.root, 
                          replace_equalities_in_formula(f.first),
                          replace_equalities_in_formula(f.second))
        else:
            return Formula(f.root, f.variable, 
                          replace_equalities_in_formula(f.statement))
    
    for formula in formulas:
        result.add(replace_equalities_in_formula(formula))

    x = next(fresh_variable_name_generator)
    y = next(fresh_variable_name_generator)
    z = next(fresh_variable_name_generator)

    reflexive = Formula('A', x, 
                       Formula('SAME', [Term(x), Term(x)]))
    result.add(reflexive)
    
    symmetric = Formula('A', x, Formula('A', y, Formula('->', Formula('SAME', [Term(x), Term(y)]), Formula('SAME', [Term(y), Term(x)]))))
    result.add(symmetric)

    transitive = Formula('A', x, Formula('A', y, Formula('A', z, Formula('->', Formula('&', Formula('SAME', [Term(x), Term(y)]), Formula('SAME', [Term(y), Term(z)])), Formula('SAME', [Term(x), Term(z)])))))
    result.add(transitive)
    
    all_relations = set()
    for formula in formulas:
        for relation, arity in formula.relations():
            all_relations.add((relation, arity))

    for relation, arity in all_relations:
        
        args1 = []
        args2 = []
        for i in range(arity):
            v1 = next(fresh_variable_name_generator)
            v2 = next(fresh_variable_name_generator)
            args1.append(v1)
            args2.append(v2)
    
        same_conjunction = None
        for i in range(arity):
            same = Formula('SAME', [Term(args1[i]), Term(args2[i])])
            if same_conjunction is None:
                same_conjunction = same
            else:
                same_conjunction = Formula('&', same, same_conjunction)
    
        r1 = Formula(relation, [Term(v) for v in args1])
        r2 = Formula(relation, [Term(v) for v in args2])
        if same_conjunction is not None:
            implication = Formula('->', Formula('&', same_conjunction, r1), r2)
        else:
            implication = Formula('->', r1, r2)
        for v in reversed(args1):
            implication = Formula('A', v, implication)
        for v in reversed(args2):
            implication = Formula('A', v, implication)
        
        result.add(implication)
    
    return result

def add_SAME_as_equality_in_model(model: Model[T]) -> Model[T]:
    """Adds an interpretation of the relation name ``'SAME'`` in the given
    model, that canonically corresponds to equality in the given model.

    Parameters:
        model: model that has no interpretation of the relation name
            ``'SAME'``, to add the interpretation to.

    Returns:
        A model obtained from the given model by adding an interpretation of the
        relation name ``'SAME'``, that contains precisely all pairs
        ``(``\\ `x`\\ ``,``\\ `x`\\ ``)`` for every element `x` of the universe of
        the given model.
    """
    assert 'SAME' not in model.relation_interpretations
    constant_interpretations = dict(model.constant_interpretations)
    relation_interpretations = dict(model.relation_interpretations)
    function_interpretations = dict(model.function_interpretations)

    same_tuples = set()
    for element in model.universe:
        same_tuples.add((element, element))
    
    relation_interpretations['SAME'] = same_tuples

    return Model(
        universe=model.universe,
        constant_interpretations=constant_interpretations,
        relation_interpretations=relation_interpretations,
        function_interpretations=function_interpretations
    )
def make_equality_as_SAME_in_model(model: Model[T]) -> Model[T]:
    """Converts the given model to a model where equality coincides with the
    interpretation of ``'SAME'`` in the given model, in the sense that any set
    of formulas holds in the returned model if and only if its canonically
    corresponding set of formulas that do not contain equality holds in the
    given model.

    Parameters:
        model: model to convert, that contains no function interpretations, and
            contains an interpretation of the relation name ``'SAME'`` that is
            reflexive, symmetric, transitive, and respected by the
            interpretations of all other relation names.

    Returns:
        A model that is a model of any set `formulas` if and only if the given
        model is a model of
        `replace_equality_with_SAME`\\ ``(``\\ `formulas`\\ ``)``. The universe of
        the returned model corresponds to the equivalence classes of the
        interpretation of ``'SAME'`` in the given model.
    """
    assert 'SAME' in model.relation_interpretations and \
           model.relation_arities['SAME'] == 2
    assert len(model.function_interpretations) == 0

    same_relation = model.relation_interpretations['SAME']

    element_to_rep = {}
    visited = set()
    
    for element in model.universe:
        if element not in visited:
            equivalence_class = {element}
            queue = [element]
            visited.add(element)
            while queue:
                current = queue.pop(0)
                for e1, e2 in same_relation:
                    if e1 == current and e2 not in visited:
                        equivalence_class.add(e2)
                        visited.add(e2)
                        queue.append(e2)
                    elif e2 == current and e1 not in visited:
                        equivalence_class.add(e1)
                        visited.add(e1)
                        queue.append(e1)
            
            rep = min(equivalence_class)
            for e in equivalence_class:
                element_to_rep[e] = rep
    
   
    new_universe = set(element_to_rep.values())
    new_constant_interpretations = {}
    for const, value in model.constant_interpretations.items():
        new_constant_interpretations[const] = element_to_rep[value]
    new_relation_interpretations = {}
    for relation, tuples in model.relation_interpretations.items():
        if relation == 'SAME':
            continue
        new_tuples = set()
        for tup in tuples:
            new_tup = tuple(element_to_rep[e] for e in tup)
            new_tuples.add(new_tup)
        new_relation_interpretations[relation] = new_tuples
    
   
    return Model(
        universe=new_universe,
        constant_interpretations=new_constant_interpretations,
        relation_interpretations=new_relation_interpretations,
        function_interpretations={}
    )