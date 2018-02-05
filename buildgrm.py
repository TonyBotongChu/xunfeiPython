#!/usr/bin/python3
# -*- coding=utf-8 -*-
from ctypes import * 
import os
import numpy as np

ASR_RES_PATH = "fo|res/asr/common.jet"
GRM_BUILD_PATH = "res/asr/GrmBuilld"
GRM_FILE = "bnf/call.bnf"

dll = cdll.LoadLibrary(os.getcwd() + "/libmsc.so") 

def build_grm_cb(ecode, info, udata):

def build_grammar(uData):
    grm_file = open(GRM_FILE, "r")
    grm_content = list(grm_file.read())
    grm_cnt_len = len(grm_content)
    grm_build_params = (
        'engine_type = local, '
        'asr_res_path = %s, '
        'sample_rate = %d, '
        'grm_build_path = %s, '
        ) % (ASR_RES_PATH, 16000, GRM_BUILD_PATH)
    print(grm_build_params)
    #print(grm_content)
    print(grm_cnt_len)
    dll.QISRBuildGrammar("bnf", grm_content, grm_cnt_len, grm_build_params, build_grm_cb, udata)

if __name__ == "__main__":
    build_grammar("haha")
