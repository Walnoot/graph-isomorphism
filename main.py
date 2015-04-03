from recolor import *
import sys

if __name__ == "__main__":
	args = sys.argv[1:]
	if(len(args) != 2):
		print("invalid arguments")
		exit(1)
	
	mode = args[0]
	path = args[1]
	if(mode == "-i"):
		print_isomorphisms(path)
	elif(mode == "-a"):
		print_automorphisms(path)
	else:
		print("unknown option")
		exit(1)
