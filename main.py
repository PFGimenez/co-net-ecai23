import outcome
import mdl
import pickle
import math
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:",sys.argv[0],"dataset model")
    else:
        dataset = sys.argv[1]
        model = sys.argv[2]
        # load the dataset
        h = outcome.Dataset(dataset)
        # load the model
        net = pickle.load(open(model,"rb"))
        # net.export("renault_big.dot")
        # compute the MDL and convert from bits to bytes
        print(math.ceil(mdl.get_MDL(net, h)/8))

