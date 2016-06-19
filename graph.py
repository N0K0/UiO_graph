class Graph:
    _dict_of_nodes = {}

    def add_node(self,node):
        self._dict_of_nodes[node.get_code()] = node

    def get_node(self,code):
        return self._dict_of_nodes.get(code)

    def __len__(self):
        return len(self._dict_of_nodes)

    def get_graph(self):
        return self._dict_of_nodes


class Node:
    _name = ''
    _code = ''
    _site = ''
    _pre_req = ''

    _related_nodes = []
    _related_nodes_reverse = []

    def __init__(self, name, code, site,pre_req):
        self._name = name
        self._code = code
        self._site = site
        self._pre_req = pre_req

    def get_code(self):
        return self._code

    def get_name(self):
        return self._name

    def get_site(self):
        return self._site

    def get_pre_req(self):
        return self._pre_req

    def get_related(self):
        return self._related_nodes

    def add_related_node(self,node):
        if node is None:
            return
        self._related_nodes.append(node)
        node.add_related_node_rev(self)

    def add_related_node_rev(self,node):
        self._related_nodes_reverse.append(node)

    def __str__(self):
        return str(self._code)

