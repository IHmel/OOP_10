
import time
import random
import matplotlib.pyplot as plt
import array
import string as str

class check_time():
    
    def __init__(self):
        self.container_type1 = list()
        self.name1 = 'ListContainer'
        self.container_type2 = array.array('Q')
        self.name2 = 'ArrayContainer'
        self.container1_time_add = []
        self.container2_time_add = []
        self.container1_time_search = []
        self.container2_time_search = []
        self.x_values_add = []
        self.x_values_search = []
        
    def time_add_experiment(self, container_type, num_elements):
        container = container_type
        start_time = time.time()    
        for i in range(num_elements):
            container.insert(0, i)    
        end_time = time.time()
        time_add=end_time - start_time
        search_keys = random.sample(range(container_size), num_searches)
        start_time = time.time()    
        for key in search_keys:
            container.index(key)    
        end_time = time.time()
        time_search =end_time - start_time
        return time_add, time_search

    def time_search_experiment(self,container_type, container_size, num_searches):
        container = container_type
        for i in range(container_size):
            container.insert(0, i)    
        search_keys = random.sample(range(container_size), num_searches)
        start_time = time.time()    
        for key in search_keys:
            container.index(key)    
        end_time = time.time()
        return end_time - start_time


    def plot_graphs(self,container1_time, container2_time, x_values, title1, title2):
        plt.plot(x_values, container1_time, label=self.name1)
        plt.plot(x_values, container2_time, label=self.name2)
        plt.xlabel("Number of Elements")
        plt.ylabel("Time (s)")
        plt.title(title1)
        plt.grid(True)
        plt.legend()
        plt.show()
        plt.plot(x_values, container1_time, label=self.name1)
        plt.plot(x_values, container2_time, label=self.name2)
        plt.xlabel("Number of Searches")
        plt.ylabel("Time (s)")
        plt.title(title2)
        plt.grid(True)
        plt.legend()
        plt.show()

    def show_plots(self):    
        for num_elements in range(1000, 10001, 1000):
            container1_time_add_experiment,container1_time_search_experiment = self.time_experiment(self.container_type1, num_elements)
            container2_time_add_experiment,container2_time_search_experiment = self.time_experiment(self.container_type2, num_elements)    
            self.container1_time_add.append(container1_time_add_experiment)
            self.container2_time_add.append(container2_time_add_experiment)
            self.container1_time_search.append(container1_time_search_experiment)
            self.container2_time_search.append(container2_time_search_experiment)
            self.x_values_add.append(num_elements)    
         
        self.plot_graphs(self.container1_time_add, self.container2_time_add, self.x_values_add, "Add", "Search")

def main():
    do = check_time()
    do.show_plots()
    
    
if __name__ == '__main__':
    main()