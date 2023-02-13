import matplotlib.pyplot as plt
import csv
import numpy as np
import pickle

plt.rcParams['figure.figsize'] = (12, 8)

def main(i):
    filename = open("input_files/1_nodes/performance_node{}.csv".format(i), "r") # specify input directory
    file = csv.DictReader(filename)
    cpu_user = []
    cpu_system = []
    cpu_idle = []
    mem_used = []
    load_avd_1m = []
    load_avg_5m = []
    load_avg_15m = []
    final_obj = []

    for col in file:
        cpu_user.append(float(col['user']))
        cpu_system.append(float(col['system']))
        cpu_idle.append(float(col['idle']))
        mem_used.append(float(col['used']))
        load_avd_1m.append(float(col['I_min']))
        load_avg_5m.append(float(col['V_min']))
        load_avg_15m.append(float(col['XV_min']))
    filename.close()

    final_mem_used = [used / (1024 * 1024) for used in mem_used] # memory conversion B --> MB

    final_obj.append(cpu_user)
    final_obj.append(cpu_system)
    final_obj.append(cpu_idle)
    final_obj.append(final_mem_used)
    final_obj.append(load_avd_1m)
    final_obj.append(load_avg_5m)
    final_obj.append(load_avg_15m)

    return final_obj


if __name__ == '__main__':

    out_files = []
    for file in range(1, 6):
        # exclude non-existing files, for example in 3 nodes scenario files from nodes 4, and 5 does not exist
        if file not in (2,3,4,5,6):
            result = main(file)
            out_files.append(result)

    tmp = open('./input_files_perf_unopt/node_1_8', 'wb') # specify output file
    pickle.dump(out_files, tmp)
    tmp.close()
