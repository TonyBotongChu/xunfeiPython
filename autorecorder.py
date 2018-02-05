#!/usr/bin/python3
# -*- coding=utf-8 -*-

from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave

from xfRecorder import Msp
import stringutils

class recorder:
    NUM_SAMPLES = 2000  # pyaudio内置缓冲大小
    SAMPLING_RATE = 16000  # 取样频率
    #LEVEL = 500  # 声音保存的阈值
    LEVEL = 4000
    COUNT_NUM = 20  # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8  # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 60  # 录音时间，单位s

    Voice_String = []
    
    msp = Msp()

    def savewav(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(np.array(self.Voice_String).tostring())
        # wf.writeframes(self.Voice_String.decode())
        wf.close()
        print('wav saved to ' + filename)

    def setRecordLevel(self, level):
        '''设置对音量的敏感度，根据实际情况选择
        建议在500-10000之间'''
        self.LEVEL = level

    def record(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=1,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []

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
                # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                #print "debug"
                if len(save_buffer) > 0:
                    self.Voice_String = save_buffer
                    save_buffer = []
                    print("Record a piece of  voice successfully!")
                    return True
        return False

    def autorecord(self):
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
                # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                #print "debug"
                if len(save_buffer) > 0:
                    print("Record a piece of  voice successfully!")
                    text = self.msp.isr(save_buffer, session_begin_params)  
                    text = stringutils.punctuationDelete(text)
                    print("punction delete: " + text)
                    save_count = 0
                    save_buffer = []


if __name__ == "__main__":
    r = recorder()
    try:
        r.autorecord()
    except Exception as e:
        print(e)
    finally:
        r.msp.logout()
        print('logout')
