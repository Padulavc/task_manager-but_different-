from platform import system
from threading import Thread
from pygame import *
from pages import *
from spaceinvaders import SpaceInvaders


class start():
    def __init__(self):
        self.font = pygame.font.Font('fonts/space_invaders.ttf', 24)
        self.screen_width = 600
        self.screen_height = 800
        self.screen = display.set_mode((screen_height, screen_width))
        self.clock = time.Clock()
        self.icons = {}
        self.background = image.load("icons/background.jpg").convert_alpha()
    def load_var(self):
        init()
        display.init()
        display.set_caption("System Data")
        self.icons = [{'func': system, 'image':'system'},
                    {'func':network,'image':'network'},
                    {'func':cpu,'image':'cpu'},
                    {'func':disk,'image':'disk'},
                    {'func':memory,'image':'memory'},
                    {'func':overview,'image':'overview'},
                    {'func':bash,'image':'bash'},
                    {'func':SpaceInvaders,'image':'SpaceInvaders'}]
        for item in self.icons:
           item['image'] = image.load("icons/{}.png".format(item['image'])).convert_alpha()
           item['image'] = transform.scale(item['image'],(60, 60))

    def index(self):
        screen.blit(self.background, (0, 0))
        x = 75
        for icon in self.icons:
            screen.blit(icon['image'], (x, 50))
            icon['Rect'] = Rect(x, 50, 60, 60)
            x += 85

    def redraw(self, actual_function=None):
        screen.blit(self.background, (0, 0))
        screen.fill((0, 0, 0))
        self.index()
        if actual_function:
            actual_function()

    def main(self):
        self.load_var()
        self.index()
        actual_function = None
        end = False
        while not end:
            self.redraw(actual_function)
            pos = mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    end = True
                    break
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for icon in self.icons:
                        if icon['Rect'].collidepoint(pos):
                            actual_function = icon['func']
                            self.redraw(actual_function)
                if event.type == KEYDOWN:
                    if event.key == 27:
                        self.redraw(actual_function)
            display.update()
            self.redraw(actual_function)
            self.clock.tick(60)
        display.quit()

if __name__ == '__main__':
    prog = start()
    mainThread = Thread(target=prog.main())
    mainThread.start()
