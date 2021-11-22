import matplotlib.pyplot as plt
import numpy as np

def main():
    proc_times = [
        ["processing times for 1 node"]
        , ["processing times for 2 nods"]
        , ...
        , ["processing times for N nodes"]
    ]
    
    proc_times_unopt = [
        ["processing times for 1 node - unoptimized flow"]
        , ["processing times for 2 nods - unoptimized flow"]
        , ...
        , ["processing times for N nods - unoptimized flow"]
    ]
    
    file_delay = np.array(["Mean file delays - optimized flow"])
    file_delay_unopt = np.array(["Mean file delays - unoptimized flow"])

    proc_times = np.mean(proc_times, 1)
    proc_times_2 = np.mean(proc_times_unopt, 1)

    node_no = np.array([1, 2, 3, 4, 5])

    plt.plot(node_no, proc_times, 'o', color='green')
    plt.plot(node_no, proc_times_2, 'o', color='red')

    plt.grid()
    plt.xlabel('Liczba węzłów w klastrze.')
    plt.ylabel('Czas przetwarzania zbioru w minutach.')
    plt.title('Ilość węzłów a czas przetwarzania.')
    plt.legend(['zoptymalizowany przepływ', 'konfiguracja domyślna'])
    plt.savefig('output_path.png')

    plt.show()

    plt.plot(node_no, file_delay, 'o', color='green')
    plt.plot(node_no, file_delay_unopt, 'o', color='red')

    plt.grid(which='minor', axis='both')
    plt.grid()
    plt.xlabel('Liczba węzłów w klastrze.')
    plt.ylabel('Sredni czas przetwarzania w sekundach.')
    plt.title('Ilość węzłów a czas przetwarzania pojedynczego pliku.')
    plt.legend(['zoptymalizowany przepływ', 'konfiguracja domyślna'])
    plt.yscale('log')
    plt.savefig('output_path.png')
    plt.show()


if __name__ == '__main__':
    main()
