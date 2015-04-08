Usage Instructions:

python main.py [-o] <mode> <file>

example: python main.py -i test_2/products72.grl
         python main.py -o -a test_2/cubes6.grl

mode:
	Can be -i, -a, or -ia.
	-i Produces the list of isomorphic pairs of the graphs specified
	-a Computes the number of automorphisms of the graphs specified
	-ia Combines -i and -a

file:
	The .grl or .gr file that will be used for the computations

-o: (Optional) Optimizes counting isomorphisms by using results of other isomorphic graphs

You can change "from gi import *" to "from fgi import *" in main.py to use fast coloring, which is faster in some cases, and slower in other