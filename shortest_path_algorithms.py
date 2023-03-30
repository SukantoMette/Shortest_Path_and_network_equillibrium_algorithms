def label_correcting(start, end, downstream_node_dict, first_thru_node):
    '''
    :param start:
    :param end:
    :param downstream_node_dict:
    :param first_thru_node:
    :return: shortest path and corresponding shortest time
    '''
    sel = [start]

    asahi = list(downstream_node_dict.keys())
    labels = {}
    for i in asahi:
        if (i == start):
            temp = {i: [0, 1]}
            labels.update(temp)
        else:
            temp = {i: [100000, -1]}
            labels.update(temp)

    # print("current labels of the nodes\n")
    # print(labels)
    # print("\n")

    a = 0
    while (a < len(sel)):
        # print("yo",sel[a])
        for i in range(len(downstream_node_dict[sel[a]])):
            # print(downstream_node_dict[a][i])
            if (labels[sel[a]][0] + downstream_node_dict[sel[a]][i][1] < labels[downstream_node_dict[sel[a]][i][0]][0]):

                labels[downstream_node_dict[sel[a]][i][0]][0] = labels[sel[a]][0] + downstream_node_dict[sel[a]][i][1]
                labels[downstream_node_dict[sel[a]][i][0]][1] = sel[a]
                if ((downstream_node_dict[sel[a]][i][0] not in sel) and (
                        downstream_node_dict[sel[a]][i][0] >= first_thru_node)):
                    # print(downstream_node_dict[a][i][0])
                    sel.append(downstream_node_dict[sel[a]][i][0])
                    # print(sel)
                    # print("hi",sel[a])

        sel.remove(sel[a])
        # print(sel)
        a = 0  # !!!!!!!!    this line is very important ,see if it is not there,u can see what its use of this line


    temp=[end]
    route=backtracking_shortest_path(end,start,labels,temp)
    route.reverse()
    # path=shortest_path(end)
    return route,labels[end][0]


def dijkstars(start, end, downstream_node_dict, first_thru_node):
    """
    :param start:
    :param end:
    :param downstream_node_dict:
    :param first_thru_node:
    :return: shortest path and corresponding shortest time
    """
    sel = [start]
    # print("initial sel",sel)
    '''creating labels dictionary for all the nodes in the graph'''
    asahi = list(downstream_node_dict.keys())
    labels = {}
    for i in asahi:
        if (i == start):  # modified on 14/06/22  from (i == 1) to (i == start)
            temp = {i: [0, 1]}
            labels.update(temp)
        else:
            temp = {i: [100000, -1]}
            labels.update(temp)

    # print("initial labels of the nodes\n")
    # print(labels)
    # print("\n")

    while (sel != []):
        # scaning sel labels for finding node which have min label
        check_labels = [labels[i][0] for i in sel]
        # print("check label",check_labels)
        min_label = min(check_labels)
        for i in range(len(check_labels)):
            if (check_labels[i] == min_label):
                pos = i
        a = sel[pos]
        # print("a",a)

        # print("downstream_node_dict[a] is   ",downstream_node_dict[a])
        for i in range(len(downstream_node_dict[a])):
            # print("downstream_node_dict[a][i] is   ",downstream_node_dict[a][i])
            if (labels[a][0] + downstream_node_dict[a][i][1] < labels[downstream_node_dict[a][i][0]][0]):

                labels[downstream_node_dict[a][i][0]][0] = labels[a][0] + downstream_node_dict[a][i][1]
                labels[downstream_node_dict[a][i][0]][1] = a
                if ((downstream_node_dict[a][i][0] not in sel) and (downstream_node_dict[a][i][
                                                                        0] >= first_thru_node)):  # modified on 14/06/22, this "and (downstream_node_dict[a][i][0]>38" is applied to accomadate the first through node concept
                    # print(downstream_node_dict[a][i][0])
                    sel.append(downstream_node_dict[a][i][0])
                    # print("sel without removing a",sel)
                    # print("hi",sel[a])

        sel.remove(a)
        # print("sel after removing a",sel)

        # print(sel)
        # a=0 #!!!!!!!!    this line is very important ,see if it is not there,u can see what its use of this line

    # print(f"\n\nlabels after running alorithm is\n")
    # print(labels)
    temp = [end]
    route=backtracking_shortest_path(end,start,labels,temp)
    route.reverse()
    return route, labels[end][0]


def backtracking_shortest_path(end,start,labels,temp):
    b = labels[end][1]
    if (b == start):
        temp.append(b)
    else:
        temp.append(b)
        backtracking_shortest_path(b,start,labels,temp)
    return temp
