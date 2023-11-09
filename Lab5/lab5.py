
import time
import random
import matplotlib.pyplot as plt
import array

def time_add_experiment(container_type, num_elements):
    container = container_type
    start_time = time.time()
  
    for i in range(num_elements):
        container.insert(0, i)
  
    end_time = time.time()
    return end_time - start_time

def time_search_experiment(container_type, container_size, num_searches):
    container = container_type
    for i in range(container_size):
        container.insert(0, i)
  
    search_keys = random.sample(range(container_size), num_searches)
    start_time = time.time()
  
    for key in search_keys:
        container.index(key)
  
    end_time = time.time()
    return end_time - start_time


def plot_graphs(container1_time, container2_time, x_values, title1, title2):
    plt.plot(x_values, container1_time, label="Container 1")
    plt.plot(x_values, container2_time, label="Container 2")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time (s)")
    plt.title(title1)
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.plot(x_values, container1_time, label="Container 1")
    plt.plot(x_values, container2_time, label="Container 2")
    plt.xlabel("Number of Searches")
    plt.ylabel("Time (s)")
    plt.title(title2)
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    container1_time_add = []
    container2_time_add = []
    container1_time_search = []
    container2_time_search = []
    x_values_add = []
    x_values_search = []
  
    for num_elements in range(1000, 10001, 1000):
        container1_time = time_add_experiment(list(), num_elements)
        container2_time = time_add_experiment(array.array('Q'), num_elements)
  
        container1_time_add.append(container1_time)
        container2_time_add.append(container2_time)
        x_values_add.append(num_elements)
  
    for num_searches in range(1000, 10001, 1000):
        container1_time = time_search_experiment(list(), 10000, num_searches)
        container2_time = time_search_experiment(array.array('Q'), 10000, num_searches)
  
        container1_time_search.append(container1_time)
        container2_time_search.append(container2_time)
        x_values_search.append(num_searches)
  
    plot_graphs(container1_time_add, container2_time_add, x_values_add, "Time Taken for Adding Elements", "Time Taken for Searching Elements")
    plot_graphs(container1_time_search, container2_time_search, x_values_search, "Time Taken for Searching Elements", "Time Taken for Searching Elements")
