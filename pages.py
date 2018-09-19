from pickle import load
import socket
import pygame
from threading import Thread
gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.font.init()
font = pygame.font.SysFont('DS-DIGI.TFF', 24, False, False)


def getanswer(request):
    gateway.sendto(request.encode('ascii'), (host, 1312))
    (answer, server) = gateway.recvfrom(2048)
    answer = load(answer)
    answer = answer.decode('ascii')
    return answer

def use_bar(percent, text, height):
    pygame.font.init()
    width = screen_width
    percent_bar = width*(percent/100)
    """barra da base"""
    pygame.draw.rect(screen, (148, 0, 211), (20, height, screen_width, 40))
    """barra de uso"""
    pygame.draw.rect(screen, (0, 220, 0), (20, height, percent_bar, 40))
    text = font.render(text, False, (0, 220, 0))
    screen.blit(text, (20, (height - 20)))

def memory():
    answer = Thread(target=getanswer('memory'))
    answer.start()
    print(answer)

    text1 = font.render('Total Memory: %s' % answer[total_memory_GB], True, (148,0,211))
    screen.blit(text1, (screen_width / 32, 150))

    text2 = font.render('Used Memory: %s' % answer[used_memory_GB], True, (148,0,211))
    screen.blit(text2, (screen_width / 32, 200))

    text3 = font.render('Free Memory: %s' % answer[free_memory_GB], True, (148, 0, 211))
    screen.blit(text3, (screen_width / 32, 250))

    text4 = font.render('Total Swap: %s' % answer[total_swap_GB], True, (148,0,211))
    screen.blit(text4, ((2*screen_width) / 3, 150))

    text5 = font.render('Used Swap: %s' % answer[used_swap_KB], True, (148,0,211))
    screen.blit(text5, ((2*screen_width) / 3, 200))

    text6 = font.render('Free Swap: %s' % answer[free_swap_GB], True, (148, 0, 211))
    screen.blit(text6, ( (2*screen_width) / 3, 250))


    memory_percent = (total_memory_GB/used_memory_GB)/100
    swap_percent = (total_swap_GB/used_swap_KB)/100
    use_bar(memory_percent, 'Memory use', 300)
    use_bar(swap_percent, 'Swap use', 400)

def cpu():

    info1 = font.render(brand, False, (0, 220, 0))
    info2 = font.render(arch, False, (0, 220, 0))
    info3 = font.render(word, False, (0, 220, 0))
    info4 = font.render(cores_all, False, (0, 220, 0))
    info5 = font.render(cores_logical, False, (0, 220, 0))
    info6 = font.render(freq_str, False, (0, 220, 0))
    screen.blit(text1, (screen_width / 32, 150))
    screen.blit(text2, (screen_width / 32, 170))
    screen.blit(text3, (screen_width / 32, 190))
    screen.blit(text4, (screen_width / 32, 210))
    screen.blit(text5, (screen_width / 32, 230))
    screen.blit(text6, (screen_width / 32, 250))
    screen.blit(info1, (screen_width / 4, 150))
    screen.blit(info2, (screen_width / 4, 170))
    screen.blit(info3, (screen_width / 4, 190))
    screen.blit(info4, (screen_width / 4, 210))
    screen.blit(info5, (screen_width / 4, 230))
    screen.blit(info6, (screen_width / 4, 250))
    use_bar(cpu_use, 'total CPU use', 300)

    ### use per cpu --------------------------------------------

    c = psutil.cpu_percent(interval=1, percpu=True)
    y = 370
    k = 1
    for i in c:
        use_bar(i, 'Core use: ', y)
        y += 70
        k += 1

def disk():

    """
            FUNÇÃO PARA VARRER CADA PARTIÇÃO

            for item in partitions:
            print('      PARTITION: ' )
            for info in item:
                print(info)

    """



    text1 = font.render('Total space:', True, (148,0,211))
    text2 = font.render('Disk using:', True, (148,0,211))
    text3 = font.render('Free space:', True, (148,0,211))
    text4 = font.render(disk_total, True, (0, 220, 0))
    text5 = font.render(disk_use, True, (0, 220, 0))
    text6 = font.render(disk_free, True, (0, 220, 0))
    screen.blit(text1, (screen_width / 32, 150))
    screen.blit(text2, (screen_width / 32, 170))
    screen.blit(text3, (screen_width / 32, 190))
    screen.blit(text4, (screen_width / 4, 150))
    screen.blit(text5, (screen_width / 4, 170))
    screen.blit(text6, (screen_width / 4, 190))
    text7 = font.render('Disk partitions: ', True, (0, 220, 0))
    screen.blit(text7, (screen_width / 32, 210))
    x = 210

    use_bar(disk.total, 'Disk Use', x)


def overview():
    text1 = font.render('OVERVIEW PAGE UNDER CONSTRUCTION', True, (0, 220, 0))
    screen.blit(text1, (screen_width / 32, 150))


def system():
    name_text = font.render(name, True, (0, 220, 0))
    system_text = font.render(system, True, (0, 220, 0))
    version_text = font.render(version, True, (0, 220, 0))
    release_text = font.render(release, True, (0, 220, 0))
    screen.blit(name_text, (screen_width / 32, 150))
    screen.blit(system_text, (screen_width / 32, 170))
    screen.blit(version_text, (screen_width / 32, 190))
    screen.blit(release_text, (screen_width / 32, 210))

    if platform.system() == 'Linux':
        distro_text = font.render(distro, True, (0, 220, 0))
        id_text = font.render(id, True, (0, 220, 0))
        sup_text = font.render(sup, True, (0, 220, 0))
        screen.blit(distro_text, (screen_width / 32, 230))
        screen.blit(id_text, (screen_width / 32, 250))
        screen.blit(sup_text, (screen_width / 32, 270))


def network():

    passage =  psutil.net_io_counters(pernic=False, nowrap=True)
    sent = str(round(passage[0]/ (1024 * 1024),3))
    recieved = str(round(passage[1]// (1024 * 1024),3))
    packout = str(int(passage[2]/1000))
    packin = str(int(passage[3]/1000))

    adress = psutil.net_if_addrs()
    x = 20
    subx = 20
    for key in adress:
        text1 = font.render(key, True, (148, 0, 211))
        screen.blit(text1, (x, 150))
        x += screen_width/3
        for k2 in adress[key]:
            t0 = 'Family: %s ' % k2[0]
            text0 = font.render(t0, False, (0, 220, 0))
            screen.blit(text1, (subx, 170))

            t1 = 'IP adress: %s ' % k2[1]
            text1 = font.render(t1, False, (0, 220, 0))
            screen.blit(text1, (subx, 190))

            t2 = 'Netmask: %s ' % k2[2]
            text2 = font.render(t2, False, (0, 220, 0))
            screen.blit(text2, (subx, 210))

            t3 = 'Broadcast: %s ' % k2[3]
            text3 = font.render(t3, False, (0, 220, 0))
            screen.blit(text3, (subx, 230))

            t4 = 'peer to peer: %s ' % k2[4]
            text4 = font.render(t4, False, (0, 220, 0))
            screen.blit(text4, (subx, 250))

            subx += screen_width/3

def bash():
    # data = os.environ
    # text1 = font.render('Homedrive', True, (148, 0, 211))
    # screen.blit(text1, (screen_width / 16, 150))
    # text2 = font.render('Homepath', True, (148, 0, 211))
    # screen.blit(text2, (screen_width/2, 150))
    #
    # x = 170
    # for key in data:
    #     key = str(key)
    #     data[key] = str(data[key])
    #     text1 = font.render(key, True, (0, 220, 0))
    #     screen.blit(text1, (screen_width/16, x))
    #     text2 = font.render(data[key], True, (0, 220, 0))
    #     screen.blit(text2, (screen_width/2, x))
    #     x += 20

    screen.blit('page under construction', (screen_width / 16, 150))