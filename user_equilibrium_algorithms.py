from shortest_path_algorithms import dijkstars
from shortest_path_algorithms import label_correcting

def demand(file):
    '''

    :param file:
    :return: no of zones
             OD demand matrix
             total OD demand
    '''
    no_of_zones = int(file.readline().split("<NUMBER OF ZONES>")[1])
    total_OD_demand = float(file.readline().split("<TOTAL OD FLOW>")[1])
    import os
    file.seek(0, os.SEEK_SET)

    data = file.read()
    import os
    file.seek(data.find("<END OF METADATA>"), os.SEEK_SET)
    file.readline()
    file.readline()
    file.readline()
    origin = file.readline()
    origin = origin[:len(origin) - 2]

    import os
    file.seek(0, os.SEEK_SET)

    a = 1
    demand_matrix = []
    while (a <= no_of_zones):
        data = file.read()
        pos = data.find(f"{origin}{a}")
        # print(pos)
        import os
        file.seek(pos, os.SEEK_SET)
        data = file.readline()
        data = file.readline()

        demand_dict = {}
        while (data != "\n"):
            line = data.split(";")
            line.pop(-1)
            for i in line:
                temp = {float(i.split(":")[0].strip()): float(i.split(":")[1].strip())}
                demand_dict.update(temp)
            data = file.readline()
        z = 1
        row = []
        while (z <= no_of_zones):
            if (z == a):
                row.append(float(0))
            else:
                row.append(demand_dict[z])
            z += 1
        demand_matrix.append(row)
        a += 1
        import os
        file.seek(0, os.SEEK_SET)
    return no_of_zones, demand_matrix, total_OD_demand

def MSA(arcs, no_of_zones, demand_matrix, downstream_node_dict, b, capacity, power, free_flow_time, total_OD_demand,code):
    '''

    :param arcs: number of arcs
    :param no_of_zones:
    :param demand_matrix:
    :param downstream_node_dict:
    :param b:
    :param capacity:
    :param power:
    :param free_flow_time:
    :param total_OD_demand:
    :return: equilibrium link flows value(x)
             relative gap (RG)
    '''

    RG = 1
    k = 1
    while (RG >= 0.0001):
        print(k,RG)
        if (k == 1):
            x = all_or_nothing_assignment(arcs, no_of_zones, demand_matrix, downstream_node_dict,code)
            time = arc_time(x, b, capacity, power, free_flow_time,arcs)
            new_downstream_node_dict = new_dict(arcs, time)
            xhat = all_or_nothing_assignment(arcs, no_of_zones, demand_matrix, new_downstream_node_dict,code)
            RG, AEC = calculate_gap(xhat, x, time, total_OD_demand)
            k += 1
        else:
            for i in range(len(arcs)):
                x[i] = (xhat[i] / k) + (x[i] * (1 - (1 / k)))  # calculating new link flow values using convex combination of previous step (x) and (xhat) values
            time = arc_time(x, b, capacity, power, free_flow_time,arcs)
            new_downstream_node_dict = new_dict(arcs, time)
            xhat = all_or_nothing_assignment(arcs, no_of_zones, demand_matrix, new_downstream_node_dict,code)
            RG, AEC = calculate_gap(xhat, x, time, total_OD_demand)
            k += 1

    # print(x)
    # print(k, RG)
    return x, RG

def frank_wolfe(arcs, no_of_zones, demand_matrix, downstream_node_dict, b, capacity, power, free_flow_time,total_OD_demand,code):
    '''

    :param arcs:
    :param no_of_zones:
    :param demand_matrix:
    :param downstream_node_dict:
    :param b:
    :param capacity:
    :param power:
    :param free_flow_time:
    :param total_OD_demand:
    :return: equilibrium link flows value(x)
             relative gap (RG)
    '''

    RG = 1
    k = 1
    while (RG >= 0.0001):
        print(k, RG)
        if (k == 1):
            x = all_or_nothing_assignment(arcs, no_of_zones, demand_matrix, downstream_node_dict,code)
            time = arc_time(x, b, capacity, power, free_flow_time,arcs)
            new_downstream_node_dict = new_dict(arcs, time)
            xhat = all_or_nothing_assignment(arcs, no_of_zones, demand_matrix, new_downstream_node_dict,code)
            RG, AEC = calculate_gap(xhat, x, time, total_OD_demand)
            k += 1
        else:
            n = bisection(x, xhat, b, capacity, power, free_flow_time,arcs)
            for i in range(len(arcs)):
                x[i] = (xhat[i] * n) + (x[i] * (1 - n))  # calculating new link flow values using convex combination of previous step (x) and (xhat) values
            time = arc_time(x, b, capacity, power, free_flow_time,arcs)
            new_downstream_node_dict = new_dict(arcs, time)
            xhat = all_or_nothing_assignment(arcs, no_of_zones, demand_matrix, new_downstream_node_dict,code)
            RG, AEC = calculate_gap(xhat, x, time, total_OD_demand)
            k += 1

    # print(x)
    # print(k, RG)
    return x, RG

def all_or_nothing_assignment(arcs, no_of_zones, demand_matrix, downstream_node_dict,code):
    '''

    :param arcs:
    :param no_of_zones:
    :param demand_matrix:
    :param downstream_node_dict:   this keeps on changing as new travel time for each link is calculated
    :return: xhat
    '''
    xhat = []
    for m in range(len(arcs)):
        xhat.append(0)

    for i in range(no_of_zones):
        for j in range(no_of_zones):
            demand = demand_matrix[i][j]
            if (demand == 0):
                continue
            if(code==3 or code==4):
                path, time = dijkstars(i + 1, j + 1, downstream_node_dict, first_thru_node=1)
            elif(code==1 or code==2):
                path, time = label_correcting(i + 1, j + 1, downstream_node_dict, first_thru_node=1)
            path_arc_list = []
            for k in range(len(path) - 1):
                path_arc_list.append([path[k], path[k + 1]])
            for l in range(len(arcs)):
                if (arcs[l] in path_arc_list):
                    xhat[l] = xhat[l] + demand
    return xhat

def arc_time(x, b, capacity, power, free_flow_time,arcs):
    '''

    :param x:
    :param b:
    :param capacity:
    :param power:
    :param free_flow_time:
    :return: arc time
    '''
    time = []
    for i in range(len(arcs)):
        a = free_flow_time[i] * (1 + (b[i] * ((x[i] / capacity[i]) ** power[i])))
        time.append(a)
    return time

def calculate_gap(xhat, x, time, total_OD_demand):
    tstt = 0
    sptt = 0
    for i in range(len(xhat)):
        tstt = tstt + (x[i] * time[i])
        sptt = sptt + (xhat[i] * time[i])
    RG = (tstt / sptt) - 1
    AEC = (tstt - sptt) / total_OD_demand
    return RG, AEC

def bisection(x, xhat, b, capacity, power, free_flow_time,arcs):
    '''

    :param x:
    :param xhat:
    :param b:
    :param capacity:
    :param power:
    :param free_flow_time:
    :return: optimal neta(n)
    '''
    n_low = 0
    n_upper = 1

    while (n_upper - n_low >= 0.000001):
        n_avg = (n_low + n_upper) * 0.5
        xconv = []
        for i in range(len(x)):
            xconv.append((n_avg * xhat[i]) + (x[i] * (1 - n_avg)))
        time = arc_time(xconv, b, capacity, power, free_flow_time,arcs)

        derivative = 0
        for i in range(len(x)):
            derivative = derivative + ((xhat[i] - x[i]) * time[i])
        if (derivative > 0):
            n_upper = n_avg
        else:
            n_low = n_avg

    return n_avg

def new_dict(arcs, time):
        '''

        :param arcs:
        :param time:
        :return: new downstream node dict
        '''
        new_downstream_node_dict = {}
        for a in range(len(arcs)):
            temp = []
            for b in range(len(arcs)):
                if (arcs[a][0] == arcs[b][0]):
                    temp.append([arcs[b][1], time[b]])
            add = {arcs[a][0]: temp}
            new_downstream_node_dict.update(add)
        return new_downstream_node_dict
