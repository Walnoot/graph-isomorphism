from basicgraphs import graph  # , GraphError, vertex, edge
import graphIO


def color_gradient(bg_1, bg_2, colors):

    # types correct?
    if not (isinstance(bg_1, graph) and isinstance(bg_2, graph)):
        print("Not two graphs provided!")
        return False

    nbs_count_2_color_num = {}
    # basic colorisation based on degrees
    for v in (bg_1.V() + bg_2.V()):
        count = len(v.nbs())
        if count not in nbs_count_2_color_num:
            nbs_count_2_color_num[count] = len(colors)
            colors[len(colors)] = []

        c = nbs_count_2_color_num[count]
        v.colornum = c
        colors[c].append(v)


def recolor(bg_1, bg_2, colors):

    # types correct?
    if not (isinstance(bg_1, graph) and isinstance(bg_2, graph)):
        print("Not two graphs provided!")
        return False

    # refinement
    changed = True
    # refine until stable
    while changed:
        changed = False
        vertex_lists = list(colors.values())
        # for each 'color' c , but actually for each value which is a list over vertexes
        for c in vertex_lists:
            # for each color with more than 1 vertex check if it can be refined
            if len(c) > 1:
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

                for item in c_list:
                    if item[0] != cur_color_definition:
                        # create new color
                        cur_color = len(colors)
                        colors[cur_color] = []
                        cur_color_definition = item[0]
                        changed = True

                    if item[1].colornum != cur_color:
                        colors[item[1].colornum].remove(item[1])
                        item[1].colornum = cur_color
                        colors[cur_color].append(item[1])

    print("Done!")
    return colors


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

    recolor(bg1, bg2, colors)


def main_2():
    colors = {}

# crefBM_2_49 : These two graphs are isomorphic
# crefBM_4_7 : 1 and 3 are isomorphic, 0 and 2 remain undecided, and all other pairs are not isomorphic.
# crefBM_4_9 : 0 and 3 are isomorphic, 1 and 2 are isomorphic, and all other pairs are not isomorphic.
# crefBM_6_15 : 0 and 1 are isomorphic, as well as 2 and 3. Graphs 4 and 5 remain undecided,
#               and all other pairs of graphs are not isomorphic


    #tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_4_7.grl', readlist=True)
    #tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_6_15.grl', readlist=True)
    tlist = graphIO.loadgraph('GI_TestInstancesWeek1/crefBM_4_4098.grl', readlist=True)

    bg1 = tlist[0][0]
    bg2 = tlist[0][1]
    color_gradient(bg1, bg2, colors)
    #print(bg1)
    #print(bg2)
    recolor(bg1, bg2, colors)

    graphIO.writeDOT(bg1, 'res_1')
    graphIO.writeDOT(bg2, 'res_2')


main_2()
