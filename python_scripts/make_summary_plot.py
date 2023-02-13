import matplotlib.pyplot as plt
import numpy as np


def main():
    # plt.rcParams.update({'font.size': 17})
    plt.rcParams.update({'figure.dpi': 200})
    # obtained results, rows - nodes, columns - iternations
    proc_times = [
        [110, 107, 118, 111, 111, 88, 94, 93]
        , [45, 47, 46, 47, 45, 50, 49, 50]
        , [33, 37, 39, 35, 38, 33, 35, 35]
        , [31, 28, 31, 31, 29, 29, 30, 29]
        , [28, 25, 27, 27, 24, 26, 27, 28]
    ]
    file_delay = np.array([102.178, 53.802, 57.051, 45.441, 39.802])
    file_delay_unopt = np.array([482.693, 1711.937, 1007.514, 723.527, 534.344])

    proc_times_unopt = [
        [107, 147, 147, 137, 165, 170, 146, 142]
        , [77, 85, 89, 86, 75, 88, 86, 85]
        , [45, 42, 44, 44, 43, 43, 44, 43]
        , [37, 37, 37, 34, 36, 37, 38, 37]
        , [31, 32, 31, 31, 31, 31, 34, 30]
    ]

    proc_times = np.mean(proc_times, 1)
    proc_times_2 = np.mean(proc_times_unopt, 1)

    node_no = np.array([1, 2, 3, 4, 5])

    plt.plot(node_no, proc_times, 'P', color='black')
    plt.plot(node_no, proc_times_2, '^', color='black')
    plt.grid()
    plt.xlabel('Number of nodes in cluster.')
    plt.ylabel('Processing time [min].')
    plt.legend(['optimised', 'default'])
    min_ylim, max_ylim = plt.ylim()
    print(range(0, int(max_ylim) + 10, 10))
    plt.yticks(range(0, int(max_ylim) + 10, 10))
    plt.xticks(range(0, 7, 1))

    plt.savefig('./images/final/summary_plot_total_time.svg', format="svg")

    plt.show()

    plt.plot(node_no, file_delay, 'P', color='black')
    plt.plot(node_no, file_delay_unopt, '^', color='black')

    plt.grid(which='minor', axis='both')
    plt.grid()
    plt.xlabel('Number of nodes in cluster.')
    plt.ylabel('Time [s].')
    plt.legend(['optimised', 'default'])
    plt.yscale('log')
    plt.xticks(range(0, 7, 1))
    plt.savefig('./images/final/summary_plot_mean_proc.svg', format="svg")
    plt.show()


if __name__ == '__main__':
    main()
