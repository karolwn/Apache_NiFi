import pickle
import numpy as np
import os
from itertools import zip_longest
import matplotlib.pyplot as plt
import matplotlib


def main(node_no, file_mask):
    plt.rcParams.update({'font.size': 15})
    plt.rcParams.update({'figure.dpi': 100})

    directory = R'./input_files_perf/'
    directory_bad = R'./input_files_perf_unopt/'

    cpu_user, cpu_system, cpu_idle, mem_used, load_avd_1m, load_avg_5m, load_avg_15m = load_files(directory, node_no, file_mask)
    cpu_user_bad, cpu_system_bad, cpu_idle_bad, mem_used_bad, load_avd_1m_bad, load_avg_5m_bad, load_avg_15m_bad = load_files(directory_bad, node_no, file_mask)

    # print(load_avd_1m_bad)
    # print(load_avg_5m_bad)
    # print(load_avg_15m_bad)

    # Calculate metrics for optimized cluster:
    # mean between test runs:
    cpu_user_avg = calculate_main(cpu_user)
    cpu_system_avg = calculate_main(cpu_system)
    cpu_idle_avg = calculate_main(cpu_idle)
    mem_used_avg = calculate_main(mem_used)
    load_avd_1m_avg = calculate_main(load_avd_1m)
    load_avg_5m_avg = calculate_main(load_avg_5m)
    load_avg_15m_avg = calculate_main(load_avg_15m)

    # standard deviation in one test run
    # cpu_user_std = calculate_std(cpu_user_avg, 0)
    # cpu_system_std = calculate_std(cpu_system_avg, 0)
    # cpu_idle_std = calculate_std(cpu_idle_avg, 0)
    # mem_used_std = calculate_std(mem_used_avg, 0)

    # standard deviation between the runs
    load_avd_1m_std = calculate_std(load_avd_1m)
    load_avg_5m_std = calculate_std(load_avg_5m)
    load_avg_15m_std = calculate_std(load_avg_15m)

    # calculate mean std in cluster
    load_avd_1m_std = calculate_main(load_avd_1m_std)
    load_avg_5m_std = calculate_main(load_avg_5m_std)
    load_avg_15m_std = calculate_main(load_avg_15m_std)

    # calculate mean load average in cluster, 2d -> 1d:
    load_avd_1m_avg = calculate_main(load_avd_1m_avg)
    load_avg_5m_avg = calculate_main(load_avg_5m_avg)
    load_avg_15m_avg = calculate_main(load_avg_15m_avg)

    # Calculate metrics for unoptimized cluster:
    # mean between test runs:
    # cpu_user_bad_avg = calculate_main(cpu_user_bad)
    # cpu_system_bad_avg = calculate_main(cpu_system_bad)
    # cpu_idle_bad_avg = calculate_main(cpu_idle_bad)
    # mem_used_bad_avg = calculate_main(mem_used_bad)
    load_avd_1m_bad_avg = calculate_main(load_avd_1m_bad)
    load_avg_5m_bad_avg = calculate_main(load_avg_5m_bad)
    load_avg_15m_bad_avg = calculate_main(load_avg_15m_bad)

    # standard deviation in one test run
    # cpu_user_bad_std = calculate_std(cpu_user_bad_avg, 0)
    # cpu_system_bad_std = calculate_std(cpu_system_bad_avg, 0)
    # cpu_idle_bad_std = calculate_std(cpu_idle_bad_avg, 0)
    # mem_used_bad_std = calculate_std(mem_used_bad_avg, 0)

    # make_tables(
    #     node_no,
    #     cpu_user_avg, cpu_system_avg, cpu_idle_avg, mem_used_avg,
    #     cpu_user_std, cpu_system_std, cpu_idle_std, mem_used_std
    # )
    #
    # make_tables(
    #     node_no,
    #     cpu_user_bad_avg, cpu_system_bad_avg, cpu_idle_bad_avg, mem_used_bad_avg,
    #     cpu_user_bad_std, cpu_system_bad_std, cpu_idle_bad_std, mem_used_bad_std
    # )

    # standard deviation between the runs
    load_avd_1m_bad_std = calculate_std(load_avd_1m_bad)
    load_avg_5m_bad_std = calculate_std(load_avg_5m_bad)
    load_avg_15m_bad_std = calculate_std(load_avg_15m_bad)

    # calculate mean std in cluster
    load_avd_1m_bad_std = calculate_main(load_avd_1m_bad_std)
    load_avg_5m_bad_std = calculate_main(load_avg_5m_bad_std)
    load_avg_15m_bad_std = calculate_main(load_avg_15m_bad_std)

    # calculate mean load average in cluster, 2d -> 1d:
    load_avd_1m_bad_avg = calculate_main(load_avd_1m_bad_avg)
    load_avg_5m_bad_avg = calculate_main(load_avg_5m_bad_avg)
    load_avg_15m_bad_avg = calculate_main(load_avg_15m_bad_avg)

    make_load_avg_plot(
        './images/final/load_avg_cluster_{}_node.svg'.format(node_no),
        (load_avd_1m_avg, load_avg_5m_avg, load_avg_15m_avg),
        (load_avd_1m_bad_avg, load_avg_5m_bad_avg, load_avg_15m_bad_avg),
        (load_avd_1m_std, load_avg_5m_std, load_avg_15m_std),
        (load_avd_1m_bad_std, load_avg_5m_bad_std, load_avg_15m_bad_std)
    )

    make_histogram(file_mask, node_no)


def load_files(directory, node_no, file_mask):
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
        load_avd_1m.append([])
        load_avg_5m.append([])
        load_avg_15m.append([])

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
                load_avd_1m[i].append(performance_data[i][4])
                load_avg_5m[i].append(performance_data[i][5])
                load_avg_15m[i].append(performance_data[i][6])

    return cpu_user, cpu_system, cpu_idle, mem_used, load_avd_1m, load_avg_5m, load_avg_15m


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
        return np.nanstd(np.array(list(zip_longest(*a)), dtype=float), axis=dim)


def make_load_avg_plot(filename, y_good, y_bad, std_good, std_bad):
    f, (ax, bx) = plt.subplots(1, 2, sharey='row', figsize=(12, 6))

    # trim data - skip performance statistics for when the processing was already finished
    new1 = y_bad[0][:-8]
    new2 = y_bad[1][:-8]
    new3 = y_bad[2][:-8]

    # new1 = y_bad[0]
    # new2 = y_bad[1]
    # new3 = y_bad[2]

    y_bad = (new1, new2, new3)

    new1 = std_bad[0][:-8]
    new2 = std_bad[1][:-8]
    new3 = std_bad[2][:-8]

    # new1 = std_bad[0]
    # new2 = std_bad[1]
    # new3 = std_bad[2]

    std_bad = (new1, new2, new3)

    ax.plot(range(0, len(y_good[0])), y_good[0], '-', color='0.1')
    ax.plot(range(0, len(y_good[1])), y_good[1], '--', color='0.1')
    ax.plot(range(0, len(y_good[2])), y_good[2], '-.', color='0.1')

    bx.plot(range(0, len(y_bad[0])), y_bad[0], '-', color='0.1')
    bx.plot(range(0, len(y_bad[1])), y_bad[1], '--', color='0.1')
    bx.plot(range(0, len(y_bad[2])), y_bad[2], '-.', color='0.1')

    ax.fill_between(range(0, len(y_good[0])), abs(y_good[0] - (2 * std_good[0])), y_good[0] + (2 * std_good[0]), alpha=0.12, color='0.0')
    ax.fill_between(range(0, len(y_good[0])), abs(y_good[1] - (2 * std_good[1])), y_good[1] + (2 * std_good[1]), alpha=0.16, color='0.0')
    ax.fill_between(range(0, len(y_good[0])), abs(y_good[2] - (2 * std_good[2])), y_good[2] + (2 * std_good[2]), alpha=0.2, color='0.0')

    bx.fill_between(range(0, len(y_bad[0])), y_bad[0] - (2 * std_bad[0]), y_bad[0] + (2 * std_bad[0]), alpha=0.12, color='0.0')
    bx.fill_between(range(0, len(y_bad[0])), y_bad[1] - (2 * std_bad[1]), y_bad[1] + (2 * std_bad[1]), alpha=0.16, color='0.0')
    bx.fill_between(range(0, len(y_bad[0])), y_bad[2] - (2 * std_bad[2]), y_bad[2] + (2 * std_bad[2]), alpha=0.2, color='0.0')

    bx.axvline(len(y_good[0]) - 1, color='k', linestyle='dashed', linewidth=1)

    # ax.legend(['1 min', '5 min', '15 min'])
    bx.legend(['1 min', '5 min', '15 min'])

    ax.set_ylabel('Value of $\it{load}$ $\it{average}$.')

    ax.set_xlabel('Minute of measurement.\n\na) optimised configuration')
    bx.set_xlabel('Minute of measurement.\n\nb) default configuration')

    ax.set_aspect('auto')
    bx.set_aspect('auto')

    ax.set_yticks(range(-1, 12 + 1, 1))
    bx.set_yticks(range(-1, 12 + 1, 1))

    ax.set_xticks(range(0, len(y_good[0]) + 1, 5))
    bx.set_xticks(range(0, len(y_bad[0]) + 1, 5))
    # bx.set_xticks(range(0, 80 + 1, 5))

    ax.grid(True)
    bx.grid(True)

    f.savefig(filename, bbox_inches='tight', format="svg")
    f.show()


# DEPRECATED - old latex table generation
def make_tables(node_cont, user, system, idle, memory, user_std, system_std, idle_std, memory_std):
    print('\\begin{table}[H]')
    print('\\begin{center}')
    print('\\caption{Wykorzystanie zasobów serwera.}')
    print('\\begin{tabular}{|| c | c | c | c | c ||}')
    print('\\hline')
    print('Nr węzła. & CPU - użytkownik [\\%]. & CPU - system [\\%]. &  CPU - bezczynność [\\%]. &  Wykorzystany RAM [MB]. \\\\')
    print('\\hline')
    for i in range(node_cont):
        print('{} & ${}\,\pm {}\,$ & ${}\,\pm {}\,$ & ${}\,\pm {}\,$ & ${}\,\pm {}\,$  \\\\\n\\hline'.format(i+1,
                                                             round(np.mean(user[i]), 2),
                                                             round(user_std[i], 2),
                                                             round(np.mean(system[i]), 2),
                                                             round(system_std[i], 2),
                                                             round(np.mean(idle[i]), 2),
                                                             round(idle_std[i], 2),
                                                             round(np.mean(memory[i]), 2),
                                                             round(memory_std[i], 2)))

    print('średnia & ${}\,\pm {}\,$ & ${}\,\pm {}\,$ & ${}\,\pm {}\,$ & ${}\,\pm {}\,$  \\\\\n\\hline'.format(
                                                                                                         round(np.mean(user), 2),
                                                                                                         round(np.mean(user_std), 2),
                                                                                                         round(np.mean(system), 2),
                                                                                                         round(np.mean(system_std), 2),
                                                                                                         round(np.mean(idle), 2),
                                                                                                         round(np.mean(idle_std), 2),
                                                                                                         round(np.mean(memory), 2),
                                                                                                         round(np.mean(memory_std), 2)))
    print('\\end{tabular}\n\\end{center}\n\\end{table}\n')


def make_histogram(file_mask, node_no):
    directory = R'./results_files_dumps/'
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

    directory = R'./results_files_dumps_unopt/'
    files = os.listdir(directory)
    times_bad = []
    for filename in files:
        if file_mask in filename:
            full_path = os.path.join(directory, filename)
            tmp = open(full_path, 'rb')
            performance_data = pickle.load(tmp)
            tmp.close()
            times_bad.append(performance_data)

    # times_1d = [item for sublist in times for item in sublist]
    times_1d = calculate_main(times, 1)
    times_bad_1d = calculate_main(times_bad, 1)

    proc_times_clean = times_1d / 1000
    proc_times_bad_clean = times_bad_1d / 1000

    percentile_up = np.percentile(proc_times_clean, 97.5)
    percentile_down = np.percentile(proc_times_clean, 2.5)

    percentile_bad_up = np.percentile(proc_times_bad_clean, 97.5)
    percentile_bad_down = np.percentile(proc_times_bad_clean, 2.5)

    mean_val = np.mean(proc_times_clean)
    mean_bad_val = np.mean(proc_times_bad_clean)

    f, (ax, bx) = plt.subplots(1, 2, sharey='row', figsize=(12, 6))

    ax.hist(proc_times_clean, bins=500, color='0.5')
    ax.grid(True)
    ax.set_xlabel('Time [s].\n\na) optimised configuration')
    ax.set_ylabel('Total count of unique articles.')

    ax.axvline(mean_val, color='k', linestyle='dashed', linewidth=1)
    ax.axvline(percentile_up, color='k', linestyle='dashed', linewidth=1)
    ax.axvline(percentile_down, color='k', linestyle='dashed', linewidth=1)

    min_ylim, max_ylim = ax.get_ylim()

    ax.text(mean_val * 1.01, max_ylim * 0.99, 'Mean: {:.3f}'.format(mean_val), rotation=270, verticalalignment='top')
    ax.text(percentile_up * 1.01, max_ylim * 0.99, '97.5%: {:.3f}'.format(percentile_up), rotation=270, verticalalignment='top')
    ax.text(percentile_down * 1.01, max_ylim * 0.99, '2.5%: {:.3f}'.format(percentile_down), rotation=270,
             verticalalignment='top')

    ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))

    bx.hist(proc_times_bad_clean, bins=500, color='0.5')
    bx.grid(True)
    bx.set_xlabel('Time [s].\n\na) default configuration')

    bx.axvline(mean_bad_val, color='k', linestyle='dashed', linewidth=1)
    bx.axvline(percentile_bad_up, color='k', linestyle='dashed', linewidth=1)
    bx.axvline(percentile_bad_down, color='k', linestyle='dashed', linewidth=1)

    min_bad_ylim, max_bad_ylim = bx.get_ylim()
    bx.text(mean_bad_val * 1.01, max_bad_ylim * 0.99, 'Mean: {:.3f}'.format(mean_bad_val), rotation=270, verticalalignment='top')
    bx.text(percentile_bad_up * 1.01, max_bad_ylim * 0.99, '97.5%: {:.3f}'.format(percentile_bad_up), rotation=270, verticalalignment='top')
    bx.text(percentile_bad_down * 1.01, max_bad_ylim * 0.99, '2.5%: {:.3f}'.format(percentile_bad_down), rotation=270,
             verticalalignment='top')

    plt.savefig('./images/final/proc_times_cit_{}_nodes.svg'.format(node_no), bbox_inches='tight', format="svg")
    f.show()

if __name__ == '__main__':
    NUMBER_OF_NODES = 5
    FILE_MASK = 'node_5'

    main(NUMBER_OF_NODES, FILE_MASK)
