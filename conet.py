import math
import mdl

class CONet:
    """ Class representing acyclic CO-nets
    """

    def __init__(self):
        self.topo_order = []

    def export(self, filename):
        """ Export the structure of the CO-net to a graphviz format
        """
        with open(filename, "w") as f:
            f.write("digraph G { \n");
            f.write("ordering=out;\n");
            for v in self.topo_order:
                best_values = {}
                for k,val in v.cot.items():
                    best_values[k] = val
                f.write(str(id(v))+" [label=\""+str(v.variable)+"\"];\n");
                for c in v.children:
                    f.write(str(id(v))+" -> "+str(id(c))+";\n");
            f.write("}\n");

    def get_model_MDL(self):
        """ Compute the MDL of the model
        """
        l = mdl.code_length_integer(len(self.topo_order)) # how many variable in total
        for n in self.topo_order:
            l += mdl.code_length_integer(len(n.parents)) # how many parents
            l += math.log2(math.comb(len(self.topo_order)-1, len(n.parents))) # parents encoding (not its own parent)
            l += len(n.cot)*math.log2(n.domain_size) # best value encoding (number of lines in the cot * how many bits to select one value in the domain)
        return l

    def get_preferred_extension(self, instance):
        """ Compute opt(o)
        """
        instance = instance.copy()
        for n in self.topo_order:
            value = instance.get(n.variable)
            if value is None:
                value_parents = tuple([instance[p.variable] for p in n.parents])
                instance[n.variable] = n.cot[value_parents]
        return instance

    def get_minimum_data(self, instance):
        """ Compute the set of instantiated variables V of opt^{-1}(o)
        opt^{-1}(o) is simply o[V]
        """
        delta = []
        for n in self.topo_order:
            value_parents = tuple([instance[p.variable] for p in n.parents])
            if instance[n.variable] != n.cot[value_parents]:
                delta.append(n.variable)
        return delta

class Node:
    """ A node of a CO-net
    """

    def __init__(self, variable, domain_size):
        self.variable = variable
        self.domain_size = domain_size
        self.cot = {} # dict. Key: parent value. Value: preferred value
        self.children = []
        self.parents = []
