class Arcs:
    ''' this constructor takes the data file and point the cursor after the meta data '''

    def __init__(self, file):
        self.file = file
        data = self.file.read()
        position_m = data.find("<END OF METADATA>")
        # print(position_m)
        import os
        self.file.seek(position_m, os.SEEK_SET)
        data = self.file.read()
        position = data.find("~")
        # print(position)
        correct_position = position_m + position
        # print(correct_position)
        self.file.seek(correct_position, os.SEEK_SET)
        # data=self.file.readline()
        # print(data)
        # self.diff_list()

    '''this function return the columns from dataset which are further used for algorithms
       ---- return arcs in the graph
       ---- returns corresponding free flow time of the arcs
       ---- value of first thru node     
       ---- b
       ---- capacity
       ---- power     '''

    def diff_list(self):
        header_line = self.file.readline()
        # print(header_line)
        header_list = header_line.split(
            "\t")  # this list have ~ at beginning and ; at end therefore remove using pop function
        # print(list)
        header_list.pop(0)
        header_list.pop(-1)  # now header_list only contain names of the header in the given data
        # print("\n\n\n")
        # print(f"the list of column names in our data is \n{header_list}")
        # print("\n\n")
        # position of the cursor in the file is after the header line

        data = self.file.readlines()
        tail_node = []
        head_node = []
        capacity = []
        length = []
        free_flow_time = []
        b = []
        power = []
        speed = []
        toll = []
        link_type = []

        for a in data:  # here "a" will take each line from the data
            tail_node.append(int(a.split("\t")[1]))
            head_node.append(int(a.split("\t")[2]))
            capacity.append(float(a.split("\t")[3]))
            length.append(float(a.split("\t")[4]))
            free_flow_time.append(float(a.split("\t")[5]))
            b.append(float(a.split("\t")[6]))
            power.append(float(a.split("\t")[7]))
            speed.append(float(a.split("\t")[8]))
            toll.append(float(a.split("\t")[9]))
            link_type.append(float(a.split("\t")[10]))

        # reading the first through node value
        import os
        self.file.seek(0, os.SEEK_SET)
        data = self.file.read()
        position_thrunode = data.find("<FIRST THRU NODE>")
        import os
        self.file.seek(position_thrunode, os.SEEK_SET)
        thru_node_line = self.file.readline()
        first_thru_node = int(thru_node_line.split(" ")[-1])

        # creating a list named arcs containing all the arcs in the graph
        arcs = []
        for i in range(len(tail_node)):
            arcs.append([tail_node[i], head_node[i]])

        return arcs, free_flow_time, first_thru_node, b, capacity, power  # returning three things
class Nodes:
    # def __init__(self):
    #     #self.file=file
    #     #super().__init__(self.file)
    #     self.downstream_nodes()
    '''this function uses arcs and corresponding free flow time to create a dictionary having key= nodes and values= list of downstream arcs
       and return downstream_arc_dict'''

    def downstream_arcs(self,arcs):
        downstream_arc_dict = {}
        a = 0
        while (a < len(self.arcs)):
            b = a
            temp = []
            while (self.arcs[a][0] == self.arcs[b][0]):
                temp.append(self.arcs[b])  # same code just here is the change
                # print(temp)
                b = b + 1
                if (b == len(self.arcs)):  # if we dont put this if condition then at end b=76 and when this is check arc[a][0]==arc[b][0] ,it will show list index out of range
                    break  # as only it have entries from 0 to 75
            add = {self.arcs[a][0]: temp}
            downstream_arc_dict.update(add)
            dummy = b
            a = dummy

        return downstream_arc_dict

    '''this function uses arcs and corresponding free flow time to create a dictionary having key= nodes and values= list of (downstream nodes and corresponding free flow time)
           and return downstream_node_dict     
           this is basically ADJANCENCY LIST'''

    def downstream_nodes(self,arcs,free_flow_time):
        downstream_node_dict = {}
        for a in range(len(arcs)):
            temp = []
            for b in range(len(arcs)):
                if (self.arcs[a][0] == self.arcs[b][0]):
                    temp.append([self.arcs[b][1], self.free_flow_time[b]])
            add = {self.arcs[a][0]: temp}
            downstream_node_dict.update(add)
        # print(downstream_node_dict)
        return downstream_node_dict
