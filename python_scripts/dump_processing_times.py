import os
import csv
import pickle


def main():
    proc_times = load_data_from_files()
    tmp = open('location to store dumped data', 'wb')
    pickle.dump(proc_times, tmp)
    tmp.close()


def load_data_from_files():
    directory = R'input_files_path'
    proc_times = []
    files = os.listdir(directory)
    total = len(files)
    i = 1
    for filename in files:
        full_path = os.path.join(directory, filename)
        with open(full_path, 'r', encoding="utf8") as f:
            try:
                loading_data = csv.DictReader(f, delimiter='|', quoting=csv.QUOTE_NONE)
                for col in loading_data:
                    try:
                        proc_times.append(float(col['procTime']))
                    except ValueError as e:
                        # print(str(e))
                        pass
                    except TypeError as e:
                        # print(str(e))
                        pass
                    except OSError as e:
                        pass
                    except FileNotFoundError as e:
                        pass
            except csv.Error as e:
                print(str(e))
            f.close()
        print('{} of {} done'.format(i, total))
        i += 1
    return proc_times


if __name__ == '__main__':
    main()