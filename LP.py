'''
Created on Nov 21, 2020

@author: Kim
'''
from pulp import *

class Node():
    def __init__(self, name, edges):
        self.name  = name
        self.edges = edges
        
    def get_name(self):
        return self.name
    
    def get_edges(self):
        return self.edges
    
    def add_edge(self, edge):
        self.edges.append(edge)

class Edge():
    def __init__(self, node1, node2, happy, stress):
        self.node1  = node1
        self.node2  = node2
        self.happy  = happy
        self.stress = stress
        
        node1_name = self.node1.get_name()
        node2_name = self.node2.get_name()
        self.name  = node1_name + "-" + node2_name       
        
    def get_name(self):
        return self.name
    
    def get_nodes(self):
        return [self.node1.get_name(), self.node2.get_name()]
    
    def get_happy(self):
        return self.happy
    
    def get_stress(self):
        return self.stress

class Proj():
    
    def __init__(self, file_name):
        self.file_name = file_name
        
        self.n     = 0
        self.s_max = 0.0
        
        self.nodes = []
        self.edges = []
    
    def read_file(self):
        file  = open(self.file_name, 'r')
        
        self.n     = int(file.readline().strip('\n'))
        self.s_max = float(file.readline().strip('\n'))
        
        for line in file:
            node_details = line.split(' ')
            
            node1_name = node_details[0]
            node2_name = node_details[1] 
            happiness  = float(node_details[2])
            stress     = float(node_details[3])
            
            node1 = self.node_exists(node1_name)
            if not node1:
                node1 = Node(node1_name, [])
                self.nodes.append(node1)
                
            node2 = self.node_exists(node2_name) 
            if not node2:
                node2 = Node(node2_name, [])
                self.nodes.append(node2)
                
            edge = Edge(node1, node2, happiness, stress)
            node1.add_edge(edge)
            node2.add_edge(edge)
            self.edges.append(edge)
            
        file.close()
    
    def node_exists(self, node_name):
        for node in self.nodes:
            if node.get_name() == node_name:
                return node
        return None
    
    def print_nodes(self):
        for node in self.nodes:
            print(node.get_name(), ":")
            for edge in node.get_edges():
                print("   ", edge.get_nodes(), edge.get_happy(), edge.get_stress())
        print()
            
    def print_edges(self):
        for edge in self.edges:
            print(edge.get_nodes(), edge.get_happy(), edge.get_stress())
        print()
        
    def LP(self):
        k = 2
        room_size = 3
        
        prob = LpProblem("Problem", LpMaximize)
        
        names = [edge.get_name() for edge in self.edges]
        
        happy     = [edge.get_happy() for edge in self.edges]
        happy_arr = dict(zip(names, happy))
        
        stress     = [edge.get_stress() for edge in self.edges]
        stress_arr = dict(zip(names, stress))
    
        # decision variables
        var = LpVariable.dicts("var", names, 0, 1, LpInteger)
            
        # objective function
        obj = [happy_arr[i] * var[i] for i in names]
        prob += lpSum(obj)
        
        # constraints
        const = [stress_arr[i] * var[i] for i in names]
        iter  = allcombinations(const, room_size)
        for i in iter:
            prob += lpSum(i) <= (self.s_max / k)
        
        # solve        
        prob.solve()
        
        # solution status
        print ("status:", LpStatus[prob.status])
        
        for val in prob.variables():
            print(val.name, "=", val.varValue)
        
        print("done!")
        
def main():
    proj = Proj("input1.txt")
    proj.read_file()
    proj.LP()

if __name__ == '__main__':
    main()