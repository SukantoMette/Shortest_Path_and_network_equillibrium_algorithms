def node_node_adjacency_matrix(downstream_node_dict,arcs):
    '''

    :param downstream_node_dict:
    :return:node_node_adjacency_matrix
    '''

    no_of_nodes = len(downstream_node_dict.keys())
    # print(f"no of nodes in the graph are \n{no_of_nodes}")
    # print("\n\n\n")

    matrix = []
    for i in range(no_of_nodes):
        ave=[]
        for j in range(no_of_nodes):
            if([i+1,j+1] in arcs):
                ave.append(1)
            else:
                ave.append(0)
        matrix.append(ave)
    return matrix

def node_arc_incidence_matrix(downstream_node_dict, arcs):
    '''

    :param downstream_node_dict:
    :param arcs:
    :return: node_arc_incidence_matrix
    '''
    nodes = list(downstream_node_dict.keys())
    mat = []
    for node in nodes:
        temp = []
        for arc in arcs:
            if (node == arc[0]):
                temp.append(1)
            elif (node == arc[1]):
                temp.append(-1)
            else:
                temp.append(0)
        mat.append(temp)
    return mat