    """Substitutes in the current term, each constant name `construct` or
        variable name `construct` that is a key in `substitution_map` with the
        term `substitution_map`\\ ``[``\\ `construct`\\ ``]``.

        Parameters:
            substitution_map: mapping defining the substitutions to be performed.
            forbidden_variables: variable names not allowed in substitution terms.

        Returns:
            The term resulting from performing all substitutions. Only
            constant name and variable name occurrences originating in the
            current term are substituted (i.e., those originating in one of the
            specified substitutions are not subjected to additional substitutions).

        Raises:
            ForbiddenVariableError: If a term that is used in the requested
                substitution contains a variable name from
                `forbidden_variables`.

        Examples:
            >>> Term.parse('f(x,c)').substitute(
            ...     {'c': Term.parse('plus(d,x)'), 'x': Term.parse('c')}, {'y'})
            f(c,plus(d,x))

            >>> Term.parse('f(x,c)').substitute(
            ...     {'c': Term.parse('plus(d,y)')}, {'y'})
            Traceback (most recent call last):
            ...
            predicates.syntax.ForbiddenVariableError: y
        """
        for construct in substitution_map:
            assert is_constant(construct) or is_variable(construct)
        for variable in forbidden_variables:
            assert is_variable(variable)
        # Task 9.1
        
        # Если текущий терм - константа или переменная, которую нужно заменить
        if self.root in substitution_map:
            sub_term = substitution_map[self.root]
            # Проверяем запрещенные переменные
            for var in sub_term.variables():
                if var in forbidden_variables:
                    raise ForbiddenVariableError(var)
            return sub_term
        
        # Если это функция - рекурсивно подставляем в аргументы
        if is_function(self.root):
            new_arguments = [arg.substitute(substitution_map, forbidden_variables) 
                            for arg in self.arguments]
            return Term(self.root, new_arguments)
        
        # Иначе возвращаем как есть
        return self