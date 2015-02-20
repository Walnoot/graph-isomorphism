from basicgraphs import graph
from graphIO import loadgraph, savegraph


def from_file(f):
    c = complement(loadgraph(f))
    savegraph(c, 'complement_' + f)
    return 'complement_' + f


def complement(g):
    c = graph()
    vertexes = {}
    for v in g.V():
        vertexes[v] = c.addvertex()
    for v in g.V():
        for u in g.V():
            if u not in v.nbs() and v != u:
                # misschien onderstaande if niet nodig:
                if not c.adj(vertexes[v], vertexes[u]):
                    c.addedge(vertexes[v], vertexes[u])
    return c