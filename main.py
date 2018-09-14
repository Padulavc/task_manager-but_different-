import psutil
import platform
import cpuinfo
import pygame
import pages
import spaceinvaders

### IMAGE UPLOAD ###

linux_icon = pygame.image.load("icons/system_icon.png")
linux_icon = pygame.transform.scale(linux_icon, (60, 60))

network_icon = pygame.image.load("icons/network_icon.png")
network_icon = pygame.transform.scale(network_icon, (60, 60))

cpu_icon = pygame.image.load("icons/cpu_icon.png")
cpu_icon = pygame.transform.scale(cpu_icon, (60, 60))

memory_icon = pygame.image.load("icons/memory_icon.png")
memory_icon = pygame.transform.scale(memory_icon, (60, 60))

disk_icon = pygame.image.load("icons/disk_icon.png")
disk_icon = pygame.transform.scale(disk_icon, (60, 60))

overview_icon = pygame.image.load("icons/overview_icon.png")
overview_icon = pygame.transform.scale(overview_icon, (60, 60))

bash_icon = pygame.image.load("icons/bash_icon.png")
bash_icon = pygame.transform.scale(bash_icon, (60, 60))

windows_icon = pygame.image.load("icons/windows_icon.png")
windows_icon = pygame.transform.scale(windows_icon, (60, 60))

mac_icon = pygame.image.load("icons/mac_icon.png")
mac_icon = pygame.transform.scale(mac_icon, (60, 60))

space_invader = pygame.image.load("icons/space_invader.png")
space_invader = pygame.transform.scale(space_invader, (60, 60))

if platform.system() == 'Linux':
    system_icon = linux_icon
elif platform.system() == 'Windows':
    system_icon = windows_icon
elif platform.system() == 'Mac OS':
    system_icon = mac_icon
global icons

game = spaceinvaders.SpaceInvaders()
icons = [{'image': system_icon, 'rect': pygame.Rect(75, 50, 60, 60), 'page': pages.system},
         {'image': network_icon, 'rect': pygame.Rect(160, 50, 60, 60), 'page': pages.network},
         {'image': cpu_icon, 'rect': pygame.Rect(245, 50, 60, 60), 'page': pages.cpu},
         {'image': disk_icon, 'rect': pygame.Rect(330, 50, 60, 60), 'page': pages.disk},
         {'image': memory_icon, 'rect': pygame.Rect(415, 50, 60, 60), 'page': pages.memory},
         {'image': overview_icon, 'rect': pygame.Rect(500, 50, 60, 60), 'page': pages.overview},
         {'image': bash_icon, 'rect': pygame.Rect(585, 50, 60, 60), 'page': pages.bash},
         {'image': space_invader, 'rect': pygame.Rect(670, 50, 60, 60), 'page': game.main}]

### PYGAME INIT ###

pygame.init()
pygame.display.init()
pygame.font.init()
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_height, screen_width))
background = pygame.image.load("icons/background.jpg")
screen.blit(background, (0, 0))
clock = pygame.time.Clock()
pygame.display.set_caption("System Data")
end = False
font = pygame.font.SysFont('DS-DIGI.TFF', 24, False, False)


### INDEX ###
def index():
    x = 75
    pos = pygame.mouse.get_pos()
    for icon in icons:
        screen.blit(icon['image'], (x, 50))
        x += 85
        # if pos == (icon['rect'][0], 50):
        #     screen.blit(icon['focus'], (icon['rect'][0], 50))

def redraw(actual_function=None):
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    index()
    if actual_function:
        actual_function()

if __name__ == '__main__':

    index()
    actual_function = None
    while not end:
        ### MAIN ###
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for icon in icons:
                    if icon['rect'].collidepoint(pos):
                        actual_function = icon['page']
                        redraw(actual_function)
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    redraw(actual_function)
        pygame.display.update()
        redraw(actual_function)
        clock.tick(60)
    pygame.display.quit()

