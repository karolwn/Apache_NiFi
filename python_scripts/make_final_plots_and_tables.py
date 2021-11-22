import pickle
import numpy as np
import os
import numpy.ma as ma
from itertools import zip_longest
import matplotlib.pyplot as plt
import time


def main(node_no, file_mask):

    directory = R'./input_files_perf_unopt/'
    files = os.listdir(directory)

    cpu_user = []
    cpu_system = []
    cpu_idle = []
    mem_used = []
    load_avd_1m = []
    load_avg_5m = []
    load_avg_15m = []

    for i in range(node_no):
        cpu_user.append([])
        cpu_system.append([])
        cpu_idle.append([])
        mem_used.append([])

    for filename in files:
        if file_mask in filename:
            full_path = os.path.join(directory, filename)
            tmp = open(full_path, 'rb')
            performance_data = pickle.load(tmp)
            tmp.close()
            for i in range(node_no):
                cpu_user[i].append(performance_data[i][0])
                cpu_system[i].append(performance_data[i][1])
                cpu_idle[i].append(performance_data[i][2])
                mem_used[i].append(performance_data[i][3])
                load_avd_1m.append(performance_data[i][4])
                load_avg_5m.append(performance_data[i][5])
                load_avg_15m.append(performance_data[i][6])

    cpu_user_avg = calculate_main(cpu_user)
    cpu_system_avg = calculate_main(cpu_system)
    cpu_idle_avg = calculate_main(cpu_idle)
    mem_used_avg = calculate_main(mem_used)
    load_avd_1m_avg = calculate_main(load_avd_1m)
    load_avg_5m_avg = calculate_main(load_avg_5m)
    load_avg_15m_avg = calculate_main(load_avg_15m)

    cpu_user_std = calculate_std(cpu_user)
    cpu_system_std = calculate_std(cpu_system)
    cpu_idle_std = calculate_std(cpu_idle)
    mem_used_std = calculate_std(mem_used)

    make_plot_cpu_and_load_avg(
        './images/final/load_avg_cluster_{}_node_unopt'.format(node_no),        # filename
        range(len(load_avd_1m_avg)),                                      # x values
        load_avd_1m_avg,                                                  # y 1
        load_avg_5m_avg,                                                  # y 2
        load_avg_15m_avg,                                                 # y 3
        'Parametr load average.',                                         # title
        'czas w minutach',                                                # x label
        'load average',                                                   # y label
        ['1 min', '5 min', '15 min'],                                     # legend
        range(0, len(load_avd_1m_avg) + 1, 10),                           # x ticks
        range(0, int(max(load_avd_1m_avg)) + 1, 1),                       # y ticks
    )

    make_tables(
        node_no,
        cpu_user_avg, cpu_system_avg, cpu_idle_avg, mem_used_avg,
        cpu_user_std, cpu_system_std, cpu_idle_std, mem_used_std
    )

    make_histogram(file_mask, node_no)


def calculate_main(a, dim=1):
    out = []
    try:
        for row in a:
            tmp = np.nanmean(np.array(list(zip_longest(*row)), dtype=float), axis=dim)
            out.append(tmp)
        return out
    except TypeError as e:
        return np.nanmean(np.array(list(zip_longest(*a)), dtype=float), axis=dim)


def calculate_std(a, dim=1):
    out = []
    try:
        for row in a:
            tmp = np.nanstd(np.array(list(zip_longest(*row)), dtype=float), axis=dim)
            out.append(tmp)
        return out
    except TypeError as e:
        return np.nanmean(np.array(list(zip_longest(*a)), dtype=float), axis=dim)


def make_plot_cpu_and_load_avg(filename, x, data_1, data_2, data_3,
              title, x_label, y_label, legend,
              x_ticks, y_ticks, ax=None):
    plt.plot(x, data_1, color='green')
    plt.plot(x, data_2, color='red')
    plt.plot(x, data_3, color='blue')
    plt.legend(legend)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()


def make_tables(node_cont, user, system, idle, memory, user_std, system_std, idle_std, memory_std):
    print('\\begin{table}[H]')
    print('\\begin{center}')
    print('\\caption{Wykorzystanie serwerów - wartości średnie uzyskane z 8 prób.}')
    print('\\begin{tabular}{|| c | c | c | c | c ||}')
    print('\\hline')
    print('Nr węzła. & CPU - użytkownik [\\%]. & CPU - system [\\%]. &  CPU - bezczynność [\\%]. &  Wykorzystany RAM [MB]. \\\\')
    print('\\hline')
    for i in range(node_cont):
        print('{} & {} & {} & {} & {}  \\\\\n\\hline'.format(i+1,
                                                             round(np.mean(user[i]), 3),
                                                             round(np.mean(system[i]), 3),
                                                             round(np.mean(idle[i]), 3),
                                                             round(np.mean(memory[i]), 3)))
    print('\\end{tabular}\n\\end{center}\n\\end{table}\n')

    print('\\begin{table}[H]')
    print('\\begin{center}')
    print('\\caption{Wykorzystanie serwerów - średnie odchylenia standardowe między 8 próbami.}')
    print('\\begin{tabular}{|| c | c | c | c | c ||}')
    print('\\hline')
    print('Nr węzła. & CPU - użytkownik. & CPU - system. &  CPU - bezczynność. &  Wykorzystany RAM \\\\')
    print('\\hline')
    for i in range(node_cont):
        print('{} & {} & {} & {} & {}  \\\\\n\\hline'.format(i+1,
                                                             round(np.mean(user_std[i]), 3),
                                                             round(np.mean(system_std[i]), 3),
                                                             round(np.mean(idle_std[i]), 3),
                                                             round(np.mean(memory_std[i]), 3)))
    print('\\end{tabular}\n\\end{center}\n\\end{table}\n')


def make_histogram(file_mask, node_no):
    directory = R'./results_files_dumps_unopt/'
    files = os.listdir(directory)
    times = []
    for filename in files:
        if file_mask in filename:
            full_path = os.path.join(directory, filename)
            tmp = open(full_path, 'rb')
            performance_data = pickle.load(tmp)
            tmp.close()
            times.append(performance_data)

    # times_1d = [item for sublist in times for item in sublist]
    times_1d = calculate_main(times, 1)
    # print(len(times_1d))
    # percentile = np.percentile(times_1d, 99)

    # print('2d --> 1d conversion start')
    # op_time = time.time()

    # proc_times_clean = [i / 1000 for i in times_1d if i < percentile]
    # print('2d --> 1d conversion done in {}'.format(time.time() - op_time))
    proc_times_clean = times_1d / 1000
    # percentile_90 = np.percentile(proc_times_clean, 90)
    # percentile_95 = np.percentile(proc_times_clean, 95)
    percentile_95 = np.percentile(proc_times_clean, 95)
    percentile_5 = np.percentile(proc_times_clean, 5)
    mean_val = np.mean(proc_times_clean)
    plt.hist(proc_times_clean, bins=500, color='green')
    plt.grid(True)
    plt.title('Rozkład czasu przetwarzania plików wejściowych.')
    plt.xlabel('czas w sekundach')
    plt.ylabel('liczba próbek')

    plt.axvline(mean_val, color='k', linestyle='dashed', linewidth=1)
    plt.axvline(percentile_5, color='r', linestyle='dashed', linewidth=1)
    plt.axvline(percentile_95, color='r', linestyle='dashed', linewidth=1)
    # plt.xticks(range(int(min(proc_times_clean)), int(max(proc_times_clean)) + 1, 2))

    min_ylim, max_ylim = plt.ylim()
    plt.text(mean_val * 1.1, max_ylim * 0.9, 'Średnia: {:.3f}'.format(mean_val), rotation=270, verticalalignment='top')
    plt.text(percentile_95 * 1.05, max_ylim * 0.9, '95%: {:.3f}'.format(percentile_95), rotation=270, verticalalignment='top')
    plt.text(percentile_5 * 1.1, max_ylim * 0.9, '5%: {:.3f}'.format(percentile_5), rotation=270,
             verticalalignment='top')

    plt.ticklabel_format(axis="y", style="sci")
    plt.savefig('./images/final/proc_times_cit_{}_nodes_unopt'.format(node_no), bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    NUMBER_OF_NODES = 5
    FILE_MASK = 'node_5_'

    main(NUMBER_OF_NODES, FILE_MASK)
