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


class Node(object):

    def __init__(self, name, code, site,pre_req):
        self._name = name
        self._code = code
        self._site = site
        self._related_nodes = []
        self._related_nodes_reverse = []

        if pre_req is not None:
            self._pre_req = pre_req
        else:
            self._pre_req = ''

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

    def add_related_node_rev(self,node):
        self._related_nodes_reverse.append(node)

    def state(self,out=False):
        output = 'Name: {0}\nCode: {1}\nSite: {2}\nPreReqs: {3}\n\n'.format(self._name,self._code,self._site,
                                                                            self._str_related_nodes())
        if out:
            print output
        return output

    def _str_related_nodes(self):
        if len(self._related_nodes) > 0:
            return ', '.join([str(x) for x in self._related_nodes])
        else:
            return ''

    def __str__(self):
       return str(self._code)

