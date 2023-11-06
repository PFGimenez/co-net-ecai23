import math
import mdl

class CONet:
    """ Class representing acyclic CO-nets
    """

    def __init__(self):
        self.topo_order = []

    def get_model_cost(self):
        """ Computes the cost of the model
        """
        l = mdl.code_length_integer(len(self.topo_order)) # how many variable in total
        for n in self.topo_order:
            l += mdl.code_length_integer(len(n.parents)) # how many parents
            l += math.log2(math.comb(len(self.topo_order)-1, len(n.parents))) # parents encoding (not its own parent)
            l += len(n.cot)*math.log2(n.domain_size) # best value encoding (number of lines in the cot * how many bits to select one value in the domain)
        return l

    def get_preferred_extension(self, instance):
        """ Computes opt(o)
        """
        instance = instance.copy() # don’t delete the original
        for n in self.topo_order:
            if n.variable not in instance:
                value_parents = tuple([instance[p.variable] for p in n.parents])
                instance[n.variable] = n.cot[value_parents] # instantiate with the most preferred value
        return instance

    def get_minimum_data(self, instance):
        """ Computes the set of instantiated variables V of opt^{-1}(o)
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
        self.cot = {} # Key: parent values tuple. Value: preferred value
        self.parents = []
