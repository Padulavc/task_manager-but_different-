import platform
from cpuinfo import get_cpu_info
from psutil import virtual_memory, swap_memory, cpu_count, cpu_freq, disk_usage, disk_partitions, users, net_if_addrs
from math import pow
import socket
from time import sleep
#from distro import linux_distribution


#####################################################################
#                                                                   #
#    SETUP: ajustements to the socket conneciton                    #
#                                                                   #
#####################################################################

gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '159.89.233.79'
gateway.bind((host, 9991))
print('server hosted at %s' % host)

#####################################################################
#                                                                   #
#    OS AND NETWORK: gather data from the host                      #
#                                                                   #
#####################################################################

def convert(dado, exp):
    """
    :param dado: input in bytes
    :param exp: math power to set the order of magnitude
        ex: set exp = 3 to convert do Giga
            set exp = 2 to convert to Mega
    :return: data converted from bytes do another order of magnitude
    """
    return round(dado / pow(1024, exp), 2)

class struct:
    def __init__(self, *args):
        pass

    def memory(self):
        """
        :return: dictionary with memory information converted
        TOTAL_MEMORY: return in Gclientigabytes
        USED_MEMORY: return in Gigabytes
        FREE_MEMORY: return in Gigabytes
        """
        memory = virtual_memory()
        total = int(memory.total)
        using = int(memory.used)
        free  = int(total - using)

        memory_data = {
            'total_memory_GB': total,
            'used_memory_GB': using,
            'free_memory_GB': free,
        }

        for data in memory_data:
            memory_data[data] = convert(memory_data[data], 3)
            memory_data[data] = '%s GB' % memory_data[data]
        return str(memory_data)

    def swap(self):
        """
        TOTAL_SWAP: return in Giabytes
        USED_SWAP: return in Kilobytes
        FREE_SWAP: return in Gigabytes
        :return:
        """
        swap = swap_memory()
        used_swap = int(swap.used)
        total_swap = int(swap.total)
        free_swap = total_swap - used_swap

        swap_data = {
        'total_swap_GB': total_swap,
        'used_swap_KB': used_swap,
        'free_swap_GB': free_swap}

        for data in swap_data:
            if data is 'used_swap':
                swap_data[data] = convert(swap_data[data], 1)
                swap_data[data] = '%s KB' % swap_data[data]
            else:
                swap_data[data] = convert(swap_data[data], 3)
                swap_data[data] = '%s GB' % swap_data[data]
        return str(swap_data)

    def cpu(self):
        """
        :return:
        """
        cpu = get_cpu_info()

        brand = cpu['brand']
        word = cpu['bits']
        arch = cpu['arch']

        cores_all = cpu_count()
        cores_physical = cpu_count(logical=False)
        cores_logical = cores_all - cores_physical

        freq = cpu_freq()
        freq_current = '%s Mhz' % round(freq.current, 2)
        min_freq = '%s Mhz' % freq.min
        max_freq = '%s Mhz' % freq.max
        cpu_data = {
            'brand' : brand,
            'word': word,
            'arch': arch,
            'total_cores': cores_all,
            'physical-cores': cores_physical,
            'logical_cores': cores_logical,
            'current_frequency': freq_current,
            'minimun_frequency': min_freq,
            'maximun_frequency':max_freq
        }

        """
        @TODO 
                    c = psutil.cpu_percent(interval=1, percpu=True)
            adicionar contagemn por cpu
        """

        return str(cpu_data)

    def disk(self):
        """
        :return:
        """
        disk = disk_usage('.')
        total = '%s GB' % convert(disk.total, 3)
        using = '%s GB' % convert(disk.used, 3)
        free = '%s GB' % convert(disk.free, 3)
        partitions = disk_partitions(all=False)
        disk_data = {
            'disk_total': total,
            'disk_used': using,
            'disk_free': free,
            'partitions': partitions
        }

        return str(disk_data)

    def system(self):
        """
        :return:
        """

        #  !linux
        user = users()
        name = platform.node()
        system = platform.system()
        version = platform.version()
        release = platform.release()

        os_data = {
            'user': user[0][0],
            'name': name,
            'system': system,
            'version': version,
            'release': release
        }

        return str(os_data)
    def linux(self):
        dist = platform.dist()
        distro = dist[0]
        id = dist[1]
        sup = dist[2]

        linux_data = {
            'distro': distro,
            'id':id,
            'sup': sup
        }

        return str(linux_data)

    def network(self):
        interfaces = net_if_addrs()
        return interfaces

if __name__ == '__main__':
    data = struct()
    end = False

    while not end:
        try:
            sign, client = gateway.recvfrom(2048)
            print('>>CLIENT %s \n REQUESTED %s \n' % (client, sign))
            sign = sign.decode('ascii')
            sleep(1)
            if sign == 'memory':
                mem = data.memory().encode('ascii')
                gateway.sendto(mem, client)
                swap = data.swap().encode('ascii')
                gateway.sendto(swap, client)
            elif sign == 'cpu':
                cpu = data.cpu().encode('ascii')
                gateway.sendto(cpu, client)
            elif sign == 'disk':
                disk = data.disk().encode('ascii')
                gateway.sendto(disk, client)
            elif sign == 'system':
                system = data.system().encode('ascii')
                gateway.sendto(system, client)
                linux = data.linux().encode('ascii')
                gateway.sendto(linux, client)
            elif sign == 'network':
                net = data.network().encode('ascii')
                gateway.sendto(net, client)
            elif sign == 'close':
                end = True
                gateway.close()
                break
            else:
                gateway.sendto('unknown'.encode('ascii'), client)

        except Exception as err:
            if err == BrokenPipeError:
                print('Broken Pipe')
                pass
            else:
                print(err)
