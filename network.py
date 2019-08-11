#!/usr/bin/env python3
import collections
import sympy

import elements as elem

class Edge(collections.namedtuple('Edge', ['u', 'v', 'element'])):
    pass


class Network:
    def __init__(self):
        super().__init__()
        self._edges = set()
        self._nodes = set()
        self._consts = set()
        self._vars = dict()
        self._symbols = set()
        self._ground_node = None
        self._incident_edges_of_node = collections.defaultdict(list)

    def add_edge(self, elem: Edge):
        if not isinstance(elem, Edge):
            raise ValueError(
                "Only edges of class Edge can be added to the Network")
        elif elem in self._edges:
            return

        u, v, _ = elem
        if self._ground_node == None:
            self._ground_node = min(u, v)
        else:
            self._ground_node = min(self._ground_node, min(u, v))

        self._nodes.add(u)
        self._nodes.add(v)
        self._incident_edges_of_node[u] += [elem]
        self._incident_edges_of_node[v] += [elem]
        self._edges.add(elem)
        self._symbols.add(elem.element.symbol)

    def add_const(self, const: sympy.Symbol):
        if not isinstance(const, sympy.Symbol):
            raise ValueError(
                "Only constants of class sympy.Symbol can be added to the Network")

        if const in self._symbols:
            raise ValueError(
                "Constant %s is already an element symbol" % const)

        self._consts.add(const)

    def add_var(self, var: elem.Element, u: int, v: int):
        if not isinstance(var, elem.Element):
            raise ValueError(
                "Only variables of class Element can be added to the Network")

        if var in self._vars:
            raise ValueError("Variable %s is already defined" % var)

        self._vars[var] = (u, v)

    @property
    def nodes(self):
        return sorted(self._nodes, key=str)

    @property
    def edges(self):
        return self._edges

    @property
    def consts(self):
        return self._consts

    @property
    def vars(self):
        return self._vars

    @property
    def nonground_nodes(self):
        return filter(lambda u: u != self.ground_node, self.nodes)

    @property
    def ground_node(self):
        if self._ground_node is None:
            raise ValueError("Set is empty, thus there is no ground node")
        return self._ground_node

    def incident_edges(self, node):
        return self._incident_edges_of_node[node]
