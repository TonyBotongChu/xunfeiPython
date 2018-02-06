#!/usr/bin/python3
# -*- coding=utf-8 -*-

import pygame
from pygame.locals import *
from pygame import USEREVENT
from sys import exit
import threading

from autorecorder import recorder

class VoiceControll(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        r = recorder()
        try:
            num = 0
            while True:
                recordtext = r.autorecord()
                event = pygame.event.Event(USEREVENT, item_id = num, text = recordtext)
                pygame.event.post(event)
                num += 1
        except Exception as e:
            print(e)
        finally:
            r.msp.logout()
            print('logout')

class EventDisplay(threading.Thread):
    def run(self):
        pygame.init()
        SCREEN_SIZE = (640, 480)
        screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

        font = pygame.font.SysFont("arial", 16)
        font_height = font.get_linesize()
        event_text = []
        while True:
            event = pygame.event.wait()
            event_text.append(str(event))
            #获得时间的名称
            event_text = event_text[int(-SCREEN_SIZE[1] / font_height):]
            #这个切片操作保证了event_text里面只保留一个屏幕的文字

            #这么写会导致无法退出，以后再改
            if event.type == QUIT:
                exit()

            screen.fill((255, 255, 255))

            y = SCREEN_SIZE[1] - font_height
            #找一个合适的起笔位置，最下面开始但是要留一行的空
            for text in reversed(event_text):
                screen.blit(font.render(text, True, (0, 0, 0)), (0, y))
                y -= font_height
                #把笔提一行

            pygame.display.update()
        
def main():
    eventdisplay = EventDisplay()
    voicecontroll = VoiceControll()
    eventdisplay.start()
    voicecontroll.start()
    eventdisplay.join()
    voicecontroll.join()

if __name__ == '__main__':
    main()