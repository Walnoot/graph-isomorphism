from basicgraphs import graph


def path(n):
    assert n > 0
    G = graph(n)
    for i in range(0, n - 1):
        G.addedge(G[i], G[i + 1])
    return G


def cycle(n):
    assert n > 0
    G = graph(n)
    for i in range(0, n - 1):
        G.addedge(G[i], G[i + 1])
    G.addedge(G[n - 1], G[0])
    return G


def complete(n):
    assert n > 0
    g = graph(n)
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            g.addedge(g[i], g[j])
    return g


def disjoint_union(g, h):
    gh = graph()
    vertices = {}

    for v in g.V() + h.V():
        vertices[v] = gh.addvertex()
    for e in g.E() + h.E():
        gh.addedge(vertices[e.head()], vertices[e.tail()])
    return gh
