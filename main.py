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


def print_automorphisms(path, optimize_iso=False):
    #optimize_iso : optimize by reusing results of isomorphic graps
    
    # count_isomorphisms requires that the given graphs are separate instances
    # one could load a graph and make a deep copy, however, since no modules may
    # be imported it is easier to load the graphs twice
    graphs1 = graphIO.loadgraph(path, readlist=True)[0]
    graphs2 = graphIO.loadgraph(path, readlist=True)[0]
    
    cache = {}
    
    checked_pairs = []
    isomorphic_pairs = []
    
    if(optimize_iso):
        for i in range(len(graphs1)):
            for j in range(len(graphs1)):
                g = graphs1[i]
                h = graphs1[j]

                pair = (i, j)
                if i != j and not (j, i) in checked_pairs:  # do not do automorphisms, do not do pairs twice
                    if count_isomorphism(g, h, stop_early=True) > 0:
                        isomorphic_pairs.append(pair)
                    checked_pairs.append(pair)
    
    print("╔═════════╦══════════════╗")
    print("║Graph    ║#Automorphisms║")
    print("╠═════════╬══════════════╣")
    for i in range(len(graphs1)):
        aut = -1
        
        if(optimize_iso):
            for g in cache:
                if((g, i) in isomorphic_pairs or (i, g) in isomorphic_pairs):
                    aut = cache[g]
                    break
        
        if(aut == -1):
            aut = count_automorphisms(graphs1[i], graphs2[i])
        
        if(optimize_iso):
            cache[i] = aut
        
        print("║{:>9}║{:>14}║".format(i, aut))
    print("╚═════════╩══════════════╝")
    
    if(optimize_iso):
        print("Isomorphic pairs:")
        for pair in isomorphic_pairs:
            print(pair)


# debug functions
def check_automorphisms_generators_time(name='cubes6', id=-1, firstPruningRule=True, secondPruningRule=True, membershipTesting=False):
    t1 = time()
    print(t1)
    check_automorphisms_generators(name, id, firstPruningRule, secondPruningRule, membershipTesting)
    t2 = time()
    print(t2)
    print('difference: ', (t2 - t1))


def check_automorphisms_generators(name='cubes6', id=-1, firstPruningRule=True, secondPruningRule=True, membershipTesting=False):
    # generate_automorphisms requires that the given graphs are separate instances
    # one could load a graph and make a deep copy, however, since no modules may
    # be imported it is easier to load the graphs twice
    tlist = graphIO.loadgraph('' + name + '', readlist=True)
    tlist2 = graphIO.loadgraph('' + name + '', readlist=True)

    ids = [id]
    if id == -1:
        ids = range(0, len(tlist[0]))

    for i in ids:
        bg1 = tlist[0][i]
        bg2 = tlist2[0][i]

        x = []
        generate_automorphisms(bg1, bg2, [], [], x, firstPruningRule, secondPruningRule, membershipTesting)
        print("Order of the graph automorphisms in " + name + "[" + str(i) + "]: " + str(permgrputil.order(x)))


if __name__ == "__main__":
    args = sys.argv[1:]
    
    optimize = False
    
    if(args[0] == "-o"):
        args = args[1:]
        optimize = True
    
    if len(args) != 2:
        print("invalid arguments")
        exit(1)

    mode = args[0]
    path = args[1]
    if mode == "-i":
        print_isomorphisms(path)
    elif mode == "-a":
        print_automorphisms(path, optimize_iso=optimize)
    elif mode == "-ia" or mode == "-ai":
        print_isomorphisms(path)
        print_automorphisms(path, optimize_iso=optimize)
    else:
        print("unknown option")
        exit(1)
