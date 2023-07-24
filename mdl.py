import math

def code_length_integer(n):
    """ Compute the length of the optimal integer encoding
    Check Rissanen, 1983
    """
    out = math.log2(2.865064)
    n+=1 # Rissanen code is for n>0, so shift by 1 to be able to encode 0
    while n > 0:
        out += math.log2(n)
        n = math.log2(n)
    return out

def get_data_MDL_one_instance(model, instance, dataset):
    """ Get the MDL of one instance
    """
    s = model.get_minimum_data(instance)
    out = code_length_integer(len(s)) # |opt^{-1}(o)|
    out += math.log2(math.comb(len(dataset.vars), len(s))) # which combination of variable to set
    for v in s:
        out += math.log2(len(dataset.domains[v]) - 1) # which value (not the optimal one)
    return out

def get_data_MDL(model, dataset):
    """ Get the MDL of a dataset
    """
    sum_score = code_length_integer(len(dataset.dataset)) # length of dataset
    for instance in dataset.uniques:
        sum_score += get_data_MDL_one_instance(model, instance, dataset)*dataset.counts[repr(instance)] # number of occurrences
    return sum_score

def get_MDL(model, dataset):
    """ Compute the total MDL (model + data)
    """
    model_MDL = model.get_model_MDL()
    data_MDL = get_data_MDL(model, dataset)
    return model_MDL + data_MDL
