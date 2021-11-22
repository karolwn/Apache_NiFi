import psutil
from time import sleep

def main():
    output_file = open("performance_node<N>.csv", "w")
    header = "user,nice,system,idle,iowait,irq,softirq,steal,guest,guest_nice,percent,used,cached,I_min,V_min,XV_min\n"
    output_file.write(header)
    try:
        while True:
            cpu = psutil.cpu_times_percent()
            mem = psutil.virtual_memory()
            avg = psutil.getloadavg()
            line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(cpu.user, cpu.nice, cpu.system, cpu.idle, cpu.iowait, cpu.irq, cpu.softirq, cpu.steal, cpu.guest, cpu.guest_nice, mem.percent, mem.used, mem.cached, avg[0], avg[1], avg[2])
            output_file.write(line)
            sleep(60)
    except KeyboardInterrupt:
        output_file.close()
        exit(0)

if __name__ == '__main__':
    main()
