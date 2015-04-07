from gi import *
import graphIO

# sys is used for argument parsing and time for benchmarking
# neither imports are used for the actual algorithms
from time import time
import sys


def print_isomorphisms(path):
    graphs = graphIO.loadgraph(path, readlist=True)[0]

    checked_pairs = []
    isomorphic_pairs = []

    for i in range(len(graphs)):
        for j in range(len(graphs)):
            g = graphs[i]
            h = graphs[j]

            pair = (i, j)
            if i != j and not (j, i) in checked_pairs:  # do not do automorphisms, do not do pairs twice
                if count_isomorphism(g, h, stop_early=True) > 0:
                    isomorphic_pairs.append(pair)
                checked_pairs.append(pair)

    isomorphic_pairs.sort()
    print("╔════════════════╗")
    print("║Isomorphic pairs║")
    print("╠════════════════╣")
    
    for pair in isomorphic_pairs:
        print("║{:>16}║".format(str(pair)))
    print("╚════════════════╝")


def print_automorphisms(path):
    # count_isomorphisms requires that the given graphs are separate instances
    # one could load a graph and make a deep copy, however, since no modules may
    # be imported it is easier to load the graphs twice
    graphs1 = graphIO.loadgraph(path, readlist=True)[0]
    graphs2 = graphIO.loadgraph(path, readlist=True)[0]

    print("╔═════════╦══════════════╗")
    print("║Graph    ║#Automorphisms║")
    print("╠═════════╬══════════════╣")
    for i in range(len(graphs1)):
        # aut = count_isomorphism(graphs1[i], graphs2[i])
        aut = count_automorphisms(graphs1[i], graphs2[i])
        
        print("║{:>9}║{:>14}║".format(i, aut))
    print("╚═════════╩══════════════╝")


# debug functions
def check_autmorphism_generators_time(name='cubes6', id=-1):
    t1 = time()
    print(t1)
    check_autmorphism_generators(name, id)
    t2 = time()
    print(t2)
    print('difference: ', (t2 - t1))


def check_autmorphism_generators(name='cubes6', id=-1):
    # generate_autmorphisms requires that the given graphs are separate instances
    # one could load a graph and make a deep copy, however, since no modules may
    # be imported it is easier to load the graphs twice
    tlist = graphIO.loadgraph('test_2/' + name + '.grl', readlist=True)
    tlist2 = graphIO.loadgraph('test_2/' + name + '.grl', readlist=True)

    ids = [id]
    if id == -1:
        ids = range(0, len(tlist[0]))

    for i in ids:
        bg1 = tlist[0][i]
        bg2 = tlist2[0][i]

        x = []
        generate_automorphisms(bg1, bg2, [], [], x)
        print("Order of the graph automorphisms in " + name + "[" + str(i) + "]: " + str(permgrputil.order(x)))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("invalid arguments")
        exit(1)

    mode = args[0]
    path = args[1]
    if mode == "-i":
        print_isomorphisms(path)
    elif mode == "-a":
        print_automorphisms(path)
    elif mode == "-ia" or mode == "-ai":
        print_isomorphisms(path)
        print_automorphisms(path)
    else:
        print("unknown option")
        exit(1)
