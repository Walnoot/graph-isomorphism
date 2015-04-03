from basicgraphs import graph  # , GraphError, vertex, edge
from datetime import datetime
import graphIO
import permgrputil
from permv2 import permutation


def color_gradient(bg_1, bg_2, colors):
    # types correct?
    if not (isinstance(bg_1, graph) and isinstance(bg_2, graph)):
        print("Not two graphs provided!")
        return False

    def count_nbs(edges):
        def inc_nbs(v):
            if hasattr(v, 'colornum'):
                v.colornum += 1
            else:
                v.colornum = 1

        for e in edges:
            inc_nbs(e.head())
            inc_nbs(e.tail())

    count_nbs(bg_1._E)  # Instead of E() we use _E so we need not set unsafe to true.
    count_nbs(bg_2._E)  # Instead of E() we use _E so we need not set unsafe to true.

    nbs_count_2_color_num = {}
    # basic colonisation based on degrees
    combined_v = bg_1._V + bg_2._V  # Instead of the safe but slow V() we use here _V
    for v in combined_v:
        count = v.colornum
        if count not in nbs_count_2_color_num:
            nbs_count_2_color_num[count] = len(colors)
            colors[len(colors)] = []

        c = nbs_count_2_color_num[count]
        v.colornum = c

        colors[c].append(v)


def recolor(colors):  # bg_1, bg_2, are not used
    """
    :param colors: Dictionary containing the coloring of two graphs which are colored together.
    :return: <False> iff unbalanced coloring is detected;
     otherwise when done returns <True>, coloring can still be unbalanced.
    """

    # # types correct?
    # if not (isinstance(bg_1, graph) and isinstance(bg_2, graph)):
    # print("Not two graphs provided!")
    # return False

    # refinement
    changed = True
    # refine until stable
    while changed:
        changed = False
        vertex_lists = list(colors.values())
        # for each 'color' c , but actually for each value which is a list over vertexes
        for c in vertex_lists:
            # if the number of vertexes is odd, the coloring is unbalanced, we can stop
            if len(c) % 2 == 1:
                return False
            else:
                c_list = []  # list with tuples ([neighbour colors], vertex)
                # for each vertex in the current list, the list of the current 'color'
                for v in c:
                    l_item = []  # list with colors of all neighbours of current vertex
                    for n in v.get_cached_nbs():
                        l_item.append(n.colornum)

                    l_item.sort()
                    c_list.append((l_item, v))
                c_list.sort()

                cur_color = c_list[0][1].colornum
                cur_color_definition = c_list[0][0]
                # Remove all vertexes from current color
                colors[cur_color] = []

                for item in c_list:
                    if item[0] != cur_color_definition:
                        # create new color
                        cur_color = len(colors)
                        colors[cur_color] = []
                        cur_color_definition = item[0]
                        changed = True

                    item[1].colornum = cur_color
                    colors[cur_color].append(item[1])

    # print("Done!")
    return True


# creates the color dict based on the colornums of the vertices in the graph
def create_color_dict(g, h):
    colors = {}
    for v in g._V:
        l = colors.get(v.colornum, [])
        l.append(v)
        colors[v.colornum] = l
    for v in h._V:
        l = colors.get(v.colornum, [])
        l.append(v)
        colors[v.colornum] = l

    return colors


# see slides lecture 2 page 23
# g and h instance of graph
def count_isomorphism(g, h, d=None, i=None, stop_early=False):
    """
    Returns the number of isomorphisms between graphs g and h. If stop_early is specified,
    the algorithm terminates as soon as an isomorphism is found, returns 1 if an isomorphism
    is found, 0 if none.
    If you want #Aut of a graph, one should create a deep copy of the graph as the second
    argument before calling this function.
    """

    if d is None:
        d = []
    if i is None:
        i = []

    # colors = {}
    # color_gradient(g, h, colors)

    def set_colors(graph, l):
        i = 0
        for v in graph:
            if v in l:
                i += 1
                v.colornum = i
            else:
                v.colornum = 0

    set_colors(g, d)
    set_colors(h, i)
    colors = create_color_dict(g, h)

    if not recolor(colors):  # recolor can return if the coloring is unbalanced
        return 0

    if defines_bijection(colors):
        return 1

    if not is_balanced(colors):  # recolor doesnt always know if the coloring is unbalanced
        return 0

    # Choose a color class C with |C| ≥ 4
    # note that c is the list of vertices, not an int representing the color
    c = None
    for color in colors.values():
        if len(color) >= 4:
            c = color
            break

    x = None  # vertex of g with color c
    for v in c:
        if v._graph is g:
            x = v
            break

    num = 0
    for y in c:
        if y._graph is h:
            num += count_isomorphism(g, h, d + [x], i + [y], stop_early=stop_early)
            if stop_early:
                if num > 0:  # found isomorphism, no need to continue if we dont care about the amount
                    return num

    return num


def is_balanced(colors):
    for vertices in colors.values():
        if len(vertices) != 0:
            num0 = 0  # amount of vertices in graph0
            num1 = 0  # amount of vertices in the other graph
            graph0 = vertices[0]._graph

            for vertex in vertices:
                if vertex._graph is graph0:
                    num0 += 1
                else:
                    num1 += 1

            if num0 != num1:
                return False

    return True


def defines_bijection(colors):
    for vertices in colors.values():
        if len(vertices) != 2:  # found a color with #vertices != 2
            return False

        if vertices[0]._graph is vertices[1]._graph:  # both vertices belong to same graph, no bijection
            return False

    return True


def create_bg1():
    bg = graph(7)
    bg.addedge(bg[0], bg[1])
    bg.addedge(bg[1], bg[2])
    bg.addedge(bg[2], bg[3])
    bg.addedge(bg[2], bg[4])
    bg.addedge(bg[3], bg[4])
    bg.addedge(bg[4], bg[5])
    bg.addedge(bg[5], bg[6])

    return bg


def create_bg2():
    bg = graph(7)
    bg.addedge(bg[0], bg[2])
    bg.addedge(bg[2], bg[3])
    bg.addedge(bg[2], bg[4])
    bg.addedge(bg[3], bg[4])
    bg.addedge(bg[1], bg[4])
    bg.addedge(bg[1], bg[5])
    bg.addedge(bg[5], bg[6])

    return bg


def main():
    colors = []
    bg1 = create_bg1()
    bg2 = create_bg2()
    color_gradient(bg1, bg2, colors)

    recolor(colors)  # bg1, bg2,


def generate_automorphisms(graph, gCopy, verticesD, verticesI, x):  # lowercamelcase #ftw #yolo
    """
    requires arguments gCopy to be a deepcopy of graph, parameters d, i and x should be []
    return type is irrelevant for the working principle of this function, that is reserved for internal purposes only
    """

    def set_colors(graph, l):
        cnt = 0
        for v in graph:
            if v in l:
                cnt += 1
                v.colornum = cnt
            else:
                v.colornum = 0

    # set original colors, only based on D and I
    set_colors(graph, verticesD)
    set_colors(gCopy, verticesI)
    colors = create_color_dict(graph, gCopy)

    if not recolor(colors):  # recolor can return if the coloring is unbalanced
        return False
    if not is_balanced(colors):  # recolor doesnt always know if the coloring is unbalanced
        return False

    # unique automorphism
    if defines_bijection(colors):
        mapping = list(range(0, len(graph._V)))
        for i in range(0, len(colors)):
            if colors[i][0] in graph:
                mapping[colors[i][0]._label] = colors[i][1]._label
            else:
                mapping[colors[i][1]._label] = colors[i][0]._label

        # print(mapping)
        # add to generating set (assuming we return to trivial node, by pruning rule #1)
        perm = permutation(len(mapping), mapping=mapping)
        if mapping != list(range(0, len(mapping))):
            x.append(perm)
        return True  # return to last visited trivial ancestor

    # multiple automorphisms

    # Choose a color class C with |C| ≥ 4
    c = None
    instBreak = False
    for color in colors.values():
        if len(color) >= 4:
            c = color
            for i in range(0, len(verticesD)):
                if verticesD[i]._label == verticesI[i]._label:
                    instBreak = True
                    break
            if instBreak:  # because my teammembers do not allow me to use a try-catch
                break

    newEl = None  # vertex of graph with color c
    for v in c:
        if v._graph is graph:
            newEl = v
            break

    # build list of vertices of gCopy to check, while also looking for a similar node as newEl
    # this guarantees that it starts with the trivial node, if possible
    checklist = []
    for v in c:
        if v._graph is gCopy:
            checklist.append(v)
            if v._label == newEl._label:
                checklist[0], checklist[len(checklist) - 1] = v, checklist[0]

    for v in checklist:
        res = generate_automorphisms(graph, gCopy, verticesD + [newEl], verticesI + [v], x)
        if res:  # return to last trivial ancestor
            for i in range(0, len(verticesD)):
                if verticesD[i]._label != verticesI[i]._label:
                    return True  # not trivial, return to last trivial ancestor

    return False


def main_2():
    # crefBM_2_49 : These two graphs are isomorphic
    # crefBM_4_7 : 1 and 3 are isomorphic, 0 and 2 remain undecided, and all other pairs are not isomorphic.
    # crefBM_4_9 : 0 and 3 are isomorphic, 1 and 2 are isomorphic, and all other pairs are not isomorphic.
    # crefBM_6_15 : 0 and 1 are isomorphic, as well as 2 and 3. Graphs 4 and 5 remain undecided,
    # and all other pairs of graphs are not isomorphic

    # tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_4_7.grl', readlist=True)
    # tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_6_15.grl', readlist=True)
    tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_4_4098.grl', readlist=True)

    bg1 = tlist[0][0]
    bg2 = tlist[0][1]
    colors = {0: bg1._V + bg2._V}
    # color_gradient(bg1, bg2, colors)
    # print(bg1)
    # print(bg2)
    print(recolor(colors))  # bg1, bg2,

    graphIO.writeDOT(bg1, 'res_1')
    graphIO.writeDOT(bg2, 'res_2')


def print_isomorphisms(path):
    graphs = graphIO.loadgraph(path, readlist=True)[0]

    checked_pairs = []
    isomorphic_pairs = []

    for i in range(len(graphs)):
        for j in range(len(graphs)):
            g = graphs[i]
            h = graphs[j]

            pair = (i, j)
            if i != j and not (j, i) in checked_pairs:  # dont do automorphisms, dont do pairs twice
                if count_isomorphism(g, h) > 0:
                    isomorphic_pairs.append(pair)
                checked_pairs.append(pair)

    isomorphic_pairs.sort()
    print("Pairs of isomorphic graphs")
    for pair in isomorphic_pairs:
        print(pair)


def check_autmorphism_generators():
    # generate_autmorphisms requires that the given graphs are separate instances
    # one could load a graph and make a deep copy, however, since no modules may
    # be imported it is easier to load the graphs twice
    tlist = graphIO.loadgraph('test_2/cubes6.grl', readlist=True)
    bg1 = tlist[0][2]
    tlist = graphIO.loadgraph('test_2/cubes6.grl', readlist=True)
    bg2 = tlist[0][2]

    x = []
    generate_automorphisms(bg1, bg2, [], [], x)
    print("Order of the graph automorphisms:", permgrputil.order(x))


def print_automorphisms(path):
    # count_isomorphisms requires that the given graphs are separate instances
    # one could load a graph and make a deep copy, however, since no modules may
    # be imported it is easier to load the graphs twice
    graphs1 = graphIO.loadgraph(path, readlist=True)[0]
    graphs2 = graphIO.loadgraph(path, readlist=True)[0]

    print("╔═════════╦══════════════╗")
    print("║Graph:   ║#Automorphisms║")
    print("╠═════════╬══════════════╣")
    for i in range(len(graphs1)):
        aut = count_isomorphism(graphs1[i], graphs2[i])
        print("║{:>9}║{:>14}║".format(i, aut))
    print("╚═════════╩══════════════╝")


def main_3():
    tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_6_15.grl', readlist=True)
    bg1 = tlist[0][4]
    bg2 = tlist[0][5]

    print(count_isomorphism(bg1, bg2, stop_early=True))

    # graphIO.writeDOT(bg1, 'res_1')
    # graphIO.writeDOT(bg2, 'res_2')


def speed_test():
    t1 = datetime.now().timestamp()
    print(t1)
    main_2()
    t2 = datetime.now().timestamp()
    print(t2)
    print('difference: ', (t2 - t1))
