"""
Includes functions for reading and writing graphs, in a very simple readable format.
 loadgraph:        reads from files
 inputgraph:    reads from terminal input / stdin
 savegraph:        writes to files
 printgraph:    writes to terminal / stdout
 writeDOT:        writes in .dot format; can be used for visualization.
 
The other functions are internal, to implement the above functions.  

The graph objects returned by loadgraph and inputgraph are by default constructed using the <graph> class in the module basicgraphs.py, but by using an optional argument you can use your own graph class (provided that it supports the same methods/interface).

This module also supports edge weighted graphs: edges should/will have an (integer) attribute <weight>. 
"""
# Version: 30-01-2015, Paul Bonsma
# updated 30-01-2015: writeDOT also writes color information for edges.
# updated 2-2-2015: writeDOT can also write directed graphs.

import basicgraphs

defaultcolorscheme = "paired12"
numcolors = 12


def readgraph(graphclass, readline):
    """
    For internal use.
    """
    options = []
    while True:
        try:
            S = readline()
            n = int(S)
            G = graphclass(n)
            break
        except ValueError:
            if len(S) > 0 and S[-1] == '\n':
                options.append(S[:-1])
            else:
                options.append(S)
    S = readline()
    edgelist = []
    try:
        while True:
            comma = S.find(',')
            if ':' in S:
                colon = S.find(':')
                edgelist.append((int(S[:comma]), int(S[comma + 1:colon]), int(S[colon + 1:])))
            else:
                edgelist.append((int(S[:comma]), int(S[comma + 1:]), None))
            S = readline()
    except Exception:
        pass
    for edge in edgelist:
        # print("Adding edge (%d,%d)"%(edge[0],edge[1]))
        e = G.addedge(G[edge[0]], G[edge[1]])
        if edge[2] != None:
            e.weight = edge[2]
    if S != '' and S[0] == '-':
        return G, options, True
    else:
        return G, options, False


def readgraphlist(graphclass, readline):
    """
    For internal use.
    """
    options = []
    L = []
    contin = True
    while contin:
        G, newoptions, contin = readgraph(graphclass, readline)
        options += newoptions
        L.append(G)
    return L, options


def loadgraph(filename, graphclass=basicgraphs.graph, readlist=False):
    """
    Reads the file <filename>, and returns the corresponding graph object.
    Optional second argument: you may use your own <graph> class, instead of
     the one from basicgraphs.py (default).
    Optional third argument: set to True if you want to read a list of graphs, and
    options included in the file. 
    In that case, the output is a 2-tuple, where the first item is a list of graphs,
    and the second is a list of options (strings).
    """
    readfile = open(filename, 'rt')

    def readln():
        S = readfile.readline()
        while len(S) > 0 and S[0] == '#':
            S = readfile.readline()
        return S

    if readlist:
        GL, options = readgraphlist(graphclass, readln)
        readfile.close()
        return GL, options
    else:
        G, options, tmp = readgraph(graphclass, readln)
        readfile.close()
        return G  # ,options


def inputgraph(graphclass=basicgraphs.graph, readlist=False):
    """
    Reads a graph from stdin, and returns the corresponding graph object.
    Optional first argument: you may use your own <graph> class, instead of
     the one from basicgraphs.py.
    Optional second argument: set to True if you want to read a list of graphs, and
    options included in the file. 
    In that case, the output is a 2-tuple, where the first item is a list of graphs,
    and the second is a list of options (strings).
    """

    def readln():
        S = input()
        while len(S) > 0 and S[0] == '#':
            S = input()
        return S

    if readlist:
        GL, options = readgraphlist(graphclass, readln)
        return GL, options
    else:
        G, options, tmp = readgraph(graphclass, readln)
        return G  # ,options


def writegraphlist(GL, writeline, options=[]):
    """
    For internal use.
    """
    # we may only write options that cannot be seen as an integer:
    for S in options:
        try:
            x = int(S)
        except ValueError:
            writeline(str(S))
    for i in range(len(GL)):
        G = GL[i]
        n = len(G.V())
        writeline('# Number of vertices:')
        writeline(str(n))
        # Give the vertices (temporary) labels from 0 to n-1:
        NL = {}
        for j in range(n):
            NL[G[j]] = j
        writeline('# Edge list:')
        for e in G.E():
            if hasattr(e, 'weight'):
                writeline(str(NL[e.tail()]) + ',' + str(NL[e.head()]) + ':' + str(e.weight))
            else:
                writeline(str(NL[e.tail()]) + ',' + str(NL[e.head()]))
        if i + 1 < len(GL):
            writeline('--- Next graph:')


def savegraph(GL, filename, options=[]):
    """
    Saves the given graph <GL> in the given <filename>.
    Optional last argument: a list of options that will be included in the 
    file header.
    Alternatively, <GL> may be a list of graphs, which are then all written to the
    file.
    """
    writefile = open(filename, 'wt')

    def writeln(S):
        writefile.write(S + '\n')

    if type(GL) is list:
        writegraphlist(GL, writeln, options)
    else:
        writegraphlist([GL], writeln, options)
    writefile.close()


def printgraph(GL, options=[]):
    """
    Writes the given graph <GL> to Stdout.
    Optional last argument: as list of options that will be included in the 
    header.
    Alternatively, <GL> may be a list of graphs, which are then all written.
    """

    def writeln(S):
        print(S)

    if type(GL) is list:
        writegraphlist(GL, writeln, options)
    else:
        writegraphlist([GL], writeln, options)


def writeDOT(G, filename, directed=False):
    """
    Writes the given graph <G> in .dot format to <filename>.
    If vertices contain attributes <label>, <colortext> or <colornum>, these are also
    included in the file. (Colortext should be something like "Blue", and a
    colornum should be an integer.)
    If edges contain an attribute <weight> (integer), these are also included in the
    file.
    Optional argument: directed. If True, then the edges are written as directed edges.
    Google GraphViz for more information on the .dot format.
    """
    writefile = open(filename, 'wt')
    if directed:
        writefile.write('digraph G {\n')
    else:
        writefile.write('graph G {\n')
    name = {}
    nextname = 0
    for v in G.V():
        name[v] = nextname
        nextname += 1
        options = 'penwidth=3,'
        if hasattr(v, 'label'):
            options += 'label="' + str(v.label) + '",'
        if hasattr(v, 'colortext'):
            options += 'color="' + v.colortext + '",'
        elif hasattr(v, 'colornum'):
            options += 'color=' + str(v.colornum % numcolors + 1) + ', colorscheme=' + defaultcolorscheme + ','
            if v.colornum >= numcolors:
                options += 'style=filled,fillcolor=' + str(v.colornum // numcolors + 1) + ','
        if len(options) > 0:
            writefile.write('    ' + str(name[v]) + ' [' + options[:-1] + ']\n')
        else:
            writefile.write('    ' + str(name[v]) + '\n')
    writefile.write('\n')

    for e in G.E():
        options = 'penwidth=2,'
        if hasattr(e, 'weight'):
            options += 'label="' + str(e.weight) + '",'
        if hasattr(e, 'colortext'):
            options += 'color="' + e.colortext + '",'
        elif hasattr(e, 'colornum'):
            options += 'color=' + str(e.colornum % numcolors + 1) + ', colorscheme=' + defaultcolorscheme + ','
            if e.colornum >= numcolors:
                options += 'style=filled,fillcolor=' + str(e.colornum // numcolors + 1) + ','
        if len(options) > 0:
            options = ' [' + options[:-1] + ']'
        if directed:
            writefile.write('    ' + str(name[e.tail()]) + ' -> ' + str(name[e.head()]) + options + '\n')
        else:
            writefile.write('    ' + str(name[e.tail()]) + '--' + str(name[e.head()]) + options + '\n')

    writefile.write('}')
    writefile.close()
