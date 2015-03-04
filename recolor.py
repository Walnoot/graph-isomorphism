from basicgraphs import GraphError, vertex, edge, graph


class Color():

    def __init__(self, index, amount, neightbours):
        self.index = index
        self.amount = amount
        self.neightbours = neightbours

    def check(self, v):
        if (not isinstance(v, vertex)):
            print("Not a vertex!")
            return False

        if (len(v.nbs()) != self.amount):
            return False

        if (self.neightbours != []):
            nbCheck = self.neightbours[:]
            nbContains = v.nbs()[:]
            for x in range(0, len(nbContains)):
                for y in range(0, len(nbCheck)):
                    if nbContains[x] == nbCheck[y]:
                        nbCheck[y] = None
                        break

            for y in range(0, len(nbCheck)):
                if nbCheck[y] is not None:
                    return False

        return True

    def createNbs(self, nbs):
        if nbs == []:
            print(
                "Warning: Overwriting existing neightbours in color+" + str(self.index) + ".")
        self.neightbours = nbs

    def __cmp__(self, other):
        return self.index - other.index

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

    def __repr__(self):
        rep_nbs = ""
        for n in self.neightbours:
            rep_nbs = rep_nbs + ("" if (rep_nbs == "") else ", ") + str(n.index)
        return "color(" + str(self.index) + "): A(" + str(self.amount) + ") + nbs (" + str(rep_nbs) + ")"


def color_gradient(bg_1, bg_2, colors):

    # types correct?
    if (not (isinstance(bg_1, graph) and isinstance(bg_2, graph))):
        print("Not two graphs provided!")
        return False

    # basic colorisation based on degrees
    for v in (bg_1.V() + bg_2.V()):
        v._label = None
        for y in colors:
            if y.check(v):
                v._label = y
        if v._label is None:
            y = Color(len(colors), len(v.nbs()), [])
            colors.append(y)
            v._label = y


def recolor(bg_1, bg_2, colors):

    # types correct?
    if (not (isinstance(bg_1, graph) and isinstance(bg_2, graph))):
        print("Not two graphs provided!")
        return False

    # refinement
    newColors = []
    while True:
        newColors = []
        for c in colors:
            # get all vertexes involved
            tVertexes = [[], []]
            for v in bg_1:
                if c.check(v):
                    tVertexes[0].append(v)
            for v in bg_2:
                if c.check(v):
                    tVertexes[1].append(v)
            combinedList = tVertexes[0] + tVertexes[1]
            if len(combinedList) == 0:
                continue

            # manipulate
            cList = []
            for v in range(0, len(combinedList)):
                lItem = []
                for n in combinedList[v].nbs():
                    lItem.append(n._label)
                lItem.sort()
                cList.append((lItem, combinedList[v]))
            cList.sort()

            # remember color at start loop and change neightbours of
            nColor = None
            colorHistory = cList[0][0]
            cList[0][1]._label.createNbs(colorHistory)

            for item in cList:
                if item[0] != colorHistory:
                    if nColor is None or not nColor.check(item[1]):
                        nColor = None
                        for cTest in colors:
                            if cTest.check(item[1]):
                                item[1]._label = cTest
                                nColor = cTest
                                break

                        if not nColor is None:
                            colorHistor = item[0]
                            nColor = Color(
                                len(colors), len(colorHistory), colorHistory)
                            colors.append(nColor)
                            newColors.append(nColor)
                            item[1]._label = nColor

                    else:
                        item[1]._label = nColor

        # no new colors: end of refining
        if len(newColors) == 0:
            print("Done!")
            break

        #colors = colors + newColors

    import pdb
    pdb.set_trace()  # breakpoint bf2f9e86 //
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
