from platform import system
import socket
from threading import Thread
from pygame import *
import pages
from spaceinvaders import SpaceInvaders


class start:
    def __init__(self):
        self.font = font.Font('fonts/space_invaders.ttf', 24)
        self.screen_width = 600
        self.screen_height = 800
        self.screen = display.set_mode((self.screen_height, self.screen_width))
        self.clock = time.Clock()
        self.icons = {}
        self.background = image.load("icons/background.jpg").convert_alpha()
        self.gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = '159.89.233.79'

    def load_var(self):
        init()
        display.init()
        display.set_caption("System Data")
        self.icons = [{'request': 'system', 'func': pages.system, 'image': 'system'},
                      {'request': 'network', 'func': pages.network, 'image': 'network'},
                      {'request': 'cpu', 'func': pages.cpu, 'image': 'cpu'},
                      {'request': 'disk', 'func': pages.disk, 'image': 'disk'},
                      {'request': 'memory', 'func': pages.memory, 'image': 'memory'},
                      {'request': 'none', 'func': pages.overview, 'image': 'overview'},
                      {'request': 'none', 'func': pages.bash, 'image': 'bash'},
                      {'request': 'none', 'func': SpaceInvaders, 'image': 'SpaceInvaders'}]
        for item in self.icons:
            item['image'] = image.load("icons/{}_icon.png".format(item['image'])).convert_alpha()
            item['image'] = transform.scale(item['image'], (60, 60))

    def index(self):
        self.screen.blit(self.background, (0, 0))
        x = 75
        for icon in self.icons:
            self.screen.blit(icon['image'], (x, 50))
            icon['Rect'] = Rect(x, 50, 60, 60)
            x += 85

    def call_server(self, request):
        self.gateway.sendto(request.encode('ascii'), (self.host, 9991))
        (answer, server) = self.gateway.recvfrom(2048)
        answer = answer.decode('ascii')
        if answer == 'unknown':
            raise Exception('Failed to retrieve answer')
        return answer

    def redraw(self, actual_function=None):
        self.screen.blit(self.background, (0, 0))
        self.screen.fill((0, 0, 0))
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
            for click in event.get():
                if click.type == QUIT:
                    end = True
                    break
                if click.type == MOUSEBUTTONDOWN and click.button == 1:
                    for icon in self.icons:
                        if icon['Rect'].collidepoint(pos):
                            try:
                                answer = self.call_server(icon['request'])
                                func = icon['func']
                                thread = Thread(target=func(), args=answer)
                                thread.start()
                                actual_function = icon['func']
                            except Exception as err:
                                handle_error = str(err)
                                print(handle_error)
                                text = self.font.render(handle_error, True, (148, 0, 211))
                                self.screen.blit(text, (self.screen_width / 32, 150))
                            self.redraw(actual_function)
                if click.type == KEYDOWN:
                    if click.key == 27:
                        self.redraw(actual_function)
            display.update()
            self.redraw(actual_function)
            self.clock.tick(60)
        display.quit()


if __name__ == '__main__':
    main = start()
    main.main()
