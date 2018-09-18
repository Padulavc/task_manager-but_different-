import platform
from cpuinfo import get_cpu_info
from psutil import virtual_memory, swap_memory, cpu_count, cpu_freq, disk_usage, disk_partitions, users, net_if_addrs
from math import pow
#####################################################################
#                                                                   #
#    SETUP: ajustements to the socket conneciton                    #
#                                                                   #
#####################################################################

#gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#host = socket.gethostname()
#gateway.bind((host, 1312))

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
        TOTAL_MEMORY: return in Gigabytes
        USED_MEMORY: return in Gigabytes
        FREE_MEMORY: return in Gigabytes
        TOTAL_SWAP: return in Giabytes
        USED_SWAP: return in Kilobytes
        FREE_SWAP: return in Gigabytes

        """
        memory = virtual_memory()
        total = int(memory.total)
        using = int(memory.used)
        free  = int(total - using)

        swap = swap_memory()
        used_swap = int(swap.used)
        total_swap = int(swap.total)
        free_swap = total_swap - used_swap

        memory_data = {
            'total_memory_GB': total,
            'used_memory_GB': using,
            'free_memory_GB': free,
            'total_swap_GB': total_swap,
            'used_swap_KB': used_swap,
            'free_swap_GB': free_swap
        }

        for data in memory_data:
            if data is 'used_swap':
                memory_data[data] = convert(memory_data[data], 1)
                memory_data[data] = '%s KB' % memory_data[data]
            else:
                memory_data[data] = convert(memory_data[data], 3)
                memory_data[data] = '%s GB' % memory_data[data]
        return memory_data

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
            c = psutil.cpu_percent(interval=1, percpu=True)
            adicionar contagemn por cpu
        """

        return cpu_data

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

        return(disk_data)

    def system(self):
        """
        :return:
        """

        #  !linux
        user = users()
        name = platform.node()
        system =  platform.system()
        version = platform.version()
        release = platform.release()

        os_data = {
            'user': user[0][0],
            'name': name,
            'system': system,
            'version': version,
            'release': release
        }

        # isLinux()
        dist = platform.dist()
        distro = dist[0]
        id = dist[1]
        sup = dist[2]

        distro = {
            'distro': distro,
            'id':id,
            'sup': sup
        }

        if system is 'Linux':  os_data += distro

        return os_data

    def network(self):
        interfaces = net_if_addrs()
        return interfaces

data = struct()
# mem = data.memory()
# print ('MEMORY DATA %s' % mem)
# cpu = data.cpu()
# print('CPU DATA %s' % cpu)
# disk = data.disk()
# print('DISK DATA %s' % disk)
# os = data.system()
# print('OS DATA %s' % os)
net = data.network()
for item in net:
    """
        get inferface
    """
    print('     -i ',item)
    for info in net[item]:
        """
            get data from the interface    
        """
        for af in info:
            print(af)