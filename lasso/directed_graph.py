from graphviz import Digraph


class DirectedGraph:

    def __init__(self):
        self.vertices = dict()
        self.edges = set()
        self.edge_to_label = dict()
        self.id = 0

    def add_vertex(self,name):
        if name not in self.vertices:
            self.vertices[name] = self.id
            self.id += 1

    def add_edge(self,source,target,label=None):
        e = (self.vertices[source],self.vertices[target])
        self.edges.add(e)
        if label is not None:
            self.edge_to_label[e] = label

    def to_dotty(self,file="out"):
        dot = Digraph()
        for v in self.vertices:
            dot.node(str(self.vertices[v]),v)
        for (s,t) in self.edges:
            if (s,t) in self.edge_to_label:
                dot.edge(str(s),str(t),self.edge_to_label[(s,t)])
            else:
                dot.edge(str(s),str(t))
        dot.render(file,view=True)