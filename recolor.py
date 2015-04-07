from basicgraphs import graph  # , GraphError, vertex, edge
import permgrputil
from permv2 import permutation
from basicpermutationgroup import Orbit


# deprecated
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


def create_color_dict(g, h):
    """
    Creates the color dict based on the colornums of the vertices in graphs g and h.
    """
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


def set_colors(graph, l):
    """
    Assigns a color to every vertex of the given graph, 0 if a vertex is not in l,
    or the index in l + 1 otherwise.
    """
    for v in graph:
        if v in l:
            for i in range(0, len(l)):
                if l[i] == v:
                    v.colornum = i + 1
                    break
        else:
            v.colornum = 0


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


def generate_automorphisms(graph, gCopy, verticesD, verticesI, x):
    """
    Requires arguments gCopy to be a deepcopy of graph, parameters d, i and x should be []
    return type is irrelevant for the working principle of this function, that is reserved for internal purposes only.
    """

    def set_colors(graph, l):
        for v in graph:
            if v in l:
                for i in range(0, len(l)):
                    if l[i] == v:
                        v.colornum = i + 1
                        break
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
    col = None
    newEl = None
    instBreak = False
    for color in colors.values():
        if len(color) >= 4:
            col = color
            for v1 in col:
                if v1._graph is graph:
                    for v2 in col:
                        if v2._graph is gCopy and v1._label == v2._label:
                            newEl = v1
                            instBreak = True
                            break
                    if instBreak:
                        break
            if instBreak:
                break

    # no trivial color has been found, thus no vertex with trivial option can be selected either
    if newEl is None:
        for v in col:
            if v._graph is graph:
                newEl = v
                break

    # build list of vertices of gCopy to check, while also looking for a similar node as newEl
    # this guarantees that it starts with the trivial node, if possible
    checklist = []
    for v in col:
        if v._graph is gCopy:
            checklist.append(v)
            if v._label == newEl._label:
                checklist[0], checklist[len(checklist) - 1] = v, checklist[0]

    # returns the orbit of an generating set and a specific element, used for the second pruning rule
    def get_orbit(x, label):
        if len(x) == 0:
            return [label]
        return Orbit(x, label)

    # calculate whether D, I is trivial, used for second pruning rule
    trivial = True
    for i in range(0, len(verticesD)):
        if verticesD[i]._label != verticesI[i]._label:
            trivial = False
            break

    for v in checklist:
        # this version of the second pruning rule only applies to branches of a trivial mapping,
        # otherwise it should not be applied checkes whether the automorphism created with mapping newEl
        # to (non trivial!) v is already produces by the generating set
        if (not trivial) or (newEl._label == v._label) or (not v._label in get_orbit(x, newEl._label)):
            res = generate_automorphisms(graph, gCopy, verticesD + [newEl], verticesI + [v], x)
            if res and not trivial:  # return to last trivial ancestor
                return True  # not trivial, return to last trivial ancestor

    # No automorphism found
    return False


def count_automorphisms(graph, graphCopy):
    x = []
    generate_automorphisms(graph, graphCopy, [], [], x)

    return permgrputil.order(x)
