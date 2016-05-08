class Graph:
    _list_of_nodes = []

    def add_node(self,node):
        self._list_of_nodes.append(node)


class Node:
    _name = ''
    _code = ''
    _site = ''

    _related_nodes = []
    _related_nodes_reverse = []

    def __init__(self, name, code, site):
        _name = name
        _code = code
        _site = site

    def get_name(self):
        return self._name

    def get_site(self):
        return self._site

    def get_related(self):
        return self._related_subjects

    def add_related_node(self,node):
        self._related_nodes.append(node)
        node.add_related_node_rev(self)

    def add_related_node_rev(self,node):
        self._related_nodes_reverse.append(node)

