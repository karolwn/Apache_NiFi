import csv
import pickle


def main(i):
    filename = open("<path to performance rports>/performance_node{}.csv".format(i), "r")
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

    final_mem_used = [used / (1024 * 1024) for used in mem_used] # memory in MB

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
        if file not in (2, 4): # exclude certain nodes (e.g. nodes weren't part of cluster)
            result = main(file)
            out_files.append(result)

    tmp = open('<output file pathc>', 'wb')
    pickle.dump(out_files, tmp)
    tmp.close()
