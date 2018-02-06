#!/usr/bin/python3
# -*- coding=utf-8 -*-

import pygame
from pygame.locals import *
from pygame import USEREVENT
from sys import exit
import threading

from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave

from xfRecorder import Msp
import stringutils

class VoiceControll(threading.Thread):
    NUM_SAMPLES = 2000  # pyaudio内置缓冲大小
    SAMPLING_RATE = 16000  # 取样频率
    #LEVEL = 500  # 声音保存的阈值
    LEVEL = 4000
    COUNT_NUM = 20  # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8  # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 60  # 录音时间，单位s

    Voice_String = []
    
    msp = Msp()

    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=1,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []

        session_begin_params = b"sub = iat, ptt = 0, result_encoding = utf8, result_type = plain, domain = iat"  
        if 16000 == self.SAMPLING_RATE:  
            session_begin_params = b"sub = iat, domain = iat, language = zh_cn, accent = mandarin, sample_rate = 16000, result_type = plain, result_encoding = utf8"  

        self.msp.login()  
        print("科大讯飞登录成功")  

        num = 0
        while True:
            # 取样
            string_audio_data = stream.read(self.NUM_SAMPLES)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum(audio_data > self.LEVEL)
            print(np.max(audio_data))
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1

            if save_count > 0:
                # 将要保存的数据存放到save_buffer中
                #print  save_count > 0 and time_count >0
                save_buffer.append(string_audio_data)
            else:
                #print save_buffer
                if len(save_buffer) > 0:
                    #print("Record a piece of  voice successfully!")
                    text = self.msp.isr(save_buffer, session_begin_params)  
                    text = stringutils.punctuationDelete(text)
                    print("punction delete: " + text)
                    save_count = 0
                    save_buffer = []
                    event = pygame.event.Event(USEREVENT, item_id = num, recordtext = text)
                    pygame.event.post(event)
                    num += 1
                    

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

def debug():
    #eventdisplay = EventDisplay()
    voicecontroll = VoiceControll()
    #eventdisplay.start()
    voicecontroll.start()
    #eventdisplay.join()
    voicecontroll.join()

if __name__ == '__main__':
    main()
    #debug()