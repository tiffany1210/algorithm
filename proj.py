'''
Created on Nov 24, 2020

@author: Kim
'''
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
    
    def __init__(self, file_name, file_output):
        self.file_name = file_name
        self.file_output = file_output
        
        self.n     = 0
        self.s_max = 0.0
        
        self.nodes = []
        self.edges = []
        
        self.rooms = []
        self.k     = 0
    
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
        
    def read_output(self):
        file  = open(self.file_output, 'r')
        for line in file:
            assign = line.split(' ')
            
            node_name = assign[0]
            room      = int(assign[1])
            
            while len(self.rooms) < room + 1:
                self.rooms.append([])
                
            self.rooms[room].append(node_name)
        
        self.k = len(self.rooms)
        file.close()
        
    def print_rooms(self):
        for room in range(len(self.rooms)):
            print(room, ": ", self.rooms[room])
        
    def calc_happiness(self):
        happy = 0.0
        for room in self.rooms:
            for i in range(len(room)):
                node1 = room[i]
                for j in range(i + 1, len(room)):
                    node2 = room[j]
                    edge = self.find_edge(node1, node2)
                    happy += edge.get_happy()
        print(happy)
        
    def check_stress(self):
        limit = self.s_max / self.k
        print("limit:", limit)
        
        for room in self.rooms:
            stress = 0.0
            for i in range(len(room)):
                node1 = room[i]
                for j in range(i + 1, len(room)):
                    node2 = room[j]
                    edge = self.find_edge(node1, node2)
                    print(node1, node2, edge.get_stress())
                    stress += edge.get_stress()
                    
                    if stress >= limit:
                        print("INVALID: stress =", stress)
                        return 
                    
        print("VALID")
        return
    
    def find_edge(self, node1, node2):
        for edge in self.edges:
            nodes = edge.get_nodes()
            if node1 in nodes and node2 in nodes:
                return edge
        return None
    
def main():
    proj = Proj("input2.txt", "output2.txt")
    proj.read_file()
    proj.read_output()
    proj.print_rooms()
    proj.calc_happiness()
    proj.check_stress()

if __name__ == '__main__':
    main()
