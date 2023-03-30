from classes import Arcs
from classes import Nodes
from user_equilibrium_algorithms import demand
from user_equilibrium_algorithms import MSA
from user_equilibrium_algorithms import frank_wolfe

import time

def input_choice():
    print("press 1 for siouxFalls network")
    print("press 2 for eastern massachusetts network")
    print("press 3 for Anaheim network")
    network_choice=int(input())

    print("press 1 for MSA-LC")
    print("press 2 for FW-LC")
    print("press 3 for MSA-LS")
    print("press 4 for FW-LS")
    code_choice = int(input())
    return code_choice,network_choice

def print_output(x,RG,time):
    print(f"equilibrium link flows is {x}")
    print(f"and the relative gap at equilibrium is {RG} ")
    print(f"time needed to run the code is {time} seconds")

def main():
    code_choice, network_choice = input_choice()

    start_time=time.time()

    if(network_choice==1):
        with open("./data_for_coding_assignment.txt", "r") as file:
            object_Arcs = Arcs(file)
            arcs, free_flow_time, first_thru_node, b, capacity, power = object_Arcs.diff_list()

        object_Nodes = Nodes()
        object_Nodes.arcs = arcs
        object_Nodes.free_flow_time = free_flow_time
        downstream_arc_dict = object_Nodes.downstream_arcs(arcs)
        downstream_node_dict = object_Nodes.downstream_nodes(arcs, free_flow_time)


        with open("./SiouxFalls_trips.tntp.txt", "r") as file:
            no_of_zones, demand_matrix, total_OD_demand = demand(file)
    elif(network_choice==2):
        with open("./eastern_mas.txt", "r") as file:
            object_Arcs = Arcs(file)
            arcs, free_flow_time, first_thru_node, b, capacity, power = object_Arcs.diff_list()

        object_Nodes = Nodes()
        object_Nodes.arcs = arcs
        object_Nodes.free_flow_time = free_flow_time
        downstream_arc_dict = object_Nodes.downstream_arcs(arcs)
        downstream_node_dict = object_Nodes.downstream_nodes(arcs, free_flow_time)

        with open("./EMA_trips.tntp.txt", "r") as file:
            no_of_zones, demand_matrix, total_OD_demand = demand(file)
    elif(network_choice==3):
        with open("./Anaheim_net.tntp.txt", "r") as file:
            object_Arcs = Arcs(file)
            arcs, free_flow_time, first_thru_node, b, capacity, power = object_Arcs.diff_list()

        object_Nodes = Nodes()
        object_Nodes.arcs = arcs
        object_Nodes.free_flow_time = free_flow_time
        downstream_arc_dict = object_Nodes.downstream_arcs(arcs)
        downstream_node_dict = object_Nodes.downstream_nodes(arcs, free_flow_time)

        with open("./Anaheim_trips.tntp.txt", "r") as file:
            no_of_zones, demand_matrix, total_OD_demand = demand(file)


    if (code_choice == 1):
        x, RG = MSA(arcs, no_of_zones, demand_matrix, downstream_node_dict, b, capacity, power, free_flow_time,total_OD_demand, code_choice)
    elif (code_choice == 2):
        x, RG = frank_wolfe(arcs, no_of_zones, demand_matrix, downstream_node_dict, b, capacity, power, free_flow_time,total_OD_demand, code_choice)
    elif (code_choice == 3):
        x, RG = MSA(arcs, no_of_zones, demand_matrix, downstream_node_dict, b, capacity, power, free_flow_time,total_OD_demand, code_choice)
    elif (code_choice == 4):
        x, RG = frank_wolfe(arcs, no_of_zones, demand_matrix, downstream_node_dict, b, capacity, power, free_flow_time,total_OD_demand, code_choice)

    end_time=time.time()
    print_output(x, RG,end_time-start_time)

if __name__ == "__main__":
    main()


