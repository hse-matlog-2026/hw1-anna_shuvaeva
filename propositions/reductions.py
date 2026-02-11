# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2025
# File name: propositions/reductions.py

"""Reduction between computational search problems."""

from __future__ import annotations
from typing import AbstractSet, Mapping, Tuple, Union

from propositions.syntax import *
from propositions.semantics import *

#: A graph on a vertex set of the form (1,...,n_vertices),
#: represented by the number of vertices n_vertices and a set of edges.
Graph = Tuple[int, AbstractSet[Tuple[int, int]]] 


def is_graph(graph: Graph) -> bool:
    (n_vertices, edges) = graph
    for edge in edges:
        for vertex in edge:
            if not 1 <= vertex <= n_vertices:
                return False
        if edge[0] == edge[1]:
            return False
    return True


def is_valid_3coloring(graph: Graph, coloring: Mapping[int, int]) -> bool:
    assert is_graph(graph)
    (n_vertices, edges) = graph
    for vertex in range(1, n_vertices + 1):
        if vertex not in coloring or coloring[vertex] not in {1, 2, 3}:
            return False
    for edge in edges:
        if coloring[edge[0]] == coloring[edge[1]]:
            return False
    return True


# ===============================
# 3-COLORING → SAT REDUCTION
# ===============================

def graph3coloring_to_formula(graph: Graph) -> Formula:
    assert is_graph(graph)
    n_vertices, edges = graph

    clauses = []

    # helper for variable x_v_c
    def var(v: int, c: int) -> Formula:
        return Formula(f'x{v}_{c}')

    # 1. each vertex has at least one color
    for v in range(1, n_vertices + 1):
        clause = Formula('|',
                         Formula('|', var(v, 1), var(v, 2)),
                         var(v, 3))
        clauses.append(clause)

    # 2. no vertex has two colors
    for v in range(1, n_vertices + 1):
        for c1 in range(1, 4):
            for c2 in range(c1 + 1, 4):
                clauses.append(
                    Formula('|',
                            Formula('~', var(v, c1)),
                            Formula('~', var(v, c2)))
                )

    # 3. adjacent vertices cannot share a color
    for (u, v) in edges:
        for c in range(1, 4):
            clauses.append(
                Formula('|',
                        Formula('~', var(u, c)),
                        Formula('~', var(v, c)))
            )

    # conjunction of all clauses
    if not clauses:
        return Formula('T')

    formula = clauses[0]
    for clause in clauses[1:]:
        formula = Formula('&', formula, clause)

    return formula


def assignment_to_3coloring(graph: Graph,
                            assignment: Model) -> Mapping[int, int]:
    assert is_graph(graph)
    n_vertices, _ = graph

    coloring = {}

    for v in range(1, n_vertices + 1):
        for c in range(1, 4):
            if assignment.get(f'x{v}_{c}', False):
                coloring[v] = c
                break

    return coloring


def tricolor_graph(graph: Graph) -> Union[Mapping[int, int], None]:
    assert is_graph(graph)
    formula = graph3coloring_to_formula(graph)
    for assignment in all_models(list(formula.variables())):
        if evaluate(formula, assignment):
            return assignment_to_3coloring(graph, assignment)
    return None
