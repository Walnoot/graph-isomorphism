from basicgraphs import graph  # , GraphError, vertex, edge
from datetime import datetime
import graphIO


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
            if len(c) % 2 != 0:
                return False
            else:
                c_list = []  # list with tuples ([neighbour colors], vertex)
                # for each vertex in the current list, the list of the current 'color'
                for v in c:
                    l_item = []  # list with colors of all neighbours of current vertex
                    for n in v.nbs():
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

#creates the color dict based on the colornums of the vertices in the graph
def create_color_dict(g, h):
    colors = {}
    for v in g._V:
        list = colors.get(v.colornum, [])
        list.append(v)
        colors[v.colornum] = list
    for v in h._V:
        list = colors.get(v.colornum, [])
        list.append(v)
        colors[v.colornum] = list
    
    return colors

#see slides lecture 2 page 23
#g and h instance of graph
def count_isomorphism(g, h, d=[], i=[]):
    #colors = {}
    #color_gradient(g, h, colors)
    
    def set_colors(graph, l):
        i=0
        for v in graph:
            if v in l:
                i += 1
                v.colornum = i
            else:
                v.colornum = 0
    
    set_colors(g, d)
    set_colors(h, i)
    colors = create_color_dict(g, h)
    
    if not recolor(colors):  #recolor can return if the coloring is unbalanced
        return 0

    if defines_bijection(colors):
        return 1

    if not is_balanced(colors):  #recolor doesnt always know if the coloring is unbalanced
        return 0
    
    #Choose a color class C with |C| ≥ 4
    #note that c is the list of vertices, not an int representing the color
    c = None
    for color in colors:
        if len(colors[color]) >= 4:
            c = colors[color]
            break
    
    x = None  #vertex of g with color c
    for v in c:
        if v._graph is g:
            x = v
            break
    
    num = 0
    for y in c:
        if y._graph is h:
            num += count_isomorphism(g, h, d+[x], i+[y])
    
    return num

def is_balanced(colors):
    for color, vertices in colors.items():
        if len(colors[color]) != 0:
            num0 = 0#amount of vertices in graph0
            num1 = 0#amount of vertices in the other graph
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
    for color, vertices in colors.items():
        if len(colors[color]) != 2:#found a color with #vertices != 2
            return False
        
        if vertices[0]._graph is vertices[1]._graph:#both vertices belong to same graph, no bijection
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


def main_2():
    colors = {}

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
    color_gradient(bg1, bg2, colors)
    # print(bg1)
    # print(bg2)
    print(recolor(colors))  # bg1, bg2,

    graphIO.writeDOT(bg1, 'res_1')
    graphIO.writeDOT(bg2, 'res_2')


def main_3():
    tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_4_7.grl', readlist=True)
    bg1 = tlist[0][0]
    bg2 = tlist[0][2]

    print(count_isomorphism(bg1, bg2))

    # graphIO.writeDOT(bg1, 'res_1')
    # graphIO.writeDOT(bg2, 'res_2')


#print(datetime.now().timestamp())
#main_2()
#print(datetime.now().timestamp())
