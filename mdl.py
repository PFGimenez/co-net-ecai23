import math

def code_length_integer(n):
    """ Computes the length of the optimal integer encoding
    Check Rissanen, 1983
    """
    l = math.log2(2.865064)
    n += 1 # Rissanen code is for n>0, so shift by 1 to be able to encode 0
    while n > 0:
        l += math.log2(n)
        n = math.log2(n)
    return l

def check_soundness(model, variables, instance):
    """ Verifies that opt(opt^{-1}(o)) = o
    """
    code = {}
    for v in variables:
        code[v] = instance[v]
    return model.get_preferred_extension(code) == instance

def get_data_MDL_one_instance(model, instance, dataset):
    """ Gets the MDL of one instance
    """
    s = model.get_minimum_data(instance)
    assert(check_soundness(model, s, instance))
    l = code_length_integer(len(s)) # |opt^{-1}(o)|
    l += math.log2(math.comb(len(dataset.vars), len(s))) # which combination of variable to set
    for v in s:
        l += math.log2(len(dataset.domains[v]) - 1) # which value (not the optimal one)
    return l

def get_data_MDL(model, dataset):
    """ Gets the MDL of a dataset
    """
    l = code_length_integer(dataset.dataset_len) # length of dataset
    for instance in dataset.uniques:
        l += get_data_MDL_one_instance(model, instance, dataset) * dataset.counts[repr(instance)] # number of occurrences
    return l

def get_MDL(model, dataset):
    """ Computes the total MDL (model + data)
    """
    model_MDL = model.get_model_MDL()
    data_MDL = get_data_MDL(model, dataset)
    return model_MDL + data_MDL
