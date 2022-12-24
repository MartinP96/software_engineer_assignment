
'''
    File name: main.py
    Version: v0.1
    Date: 23.12.2022
    Desc: Main python script file for software engineer assignment
'''

import time
from encoder_interface import EncoderInterface

if __name__ == '__main__':

    biss_bits_len = 64
    biss_mt_len = 16
    biss_st_len = 19

    encoder_interface = EncoderInterface(biss_bits_len, biss_mt_len, biss_st_len)

    while 1:

        encoder_data = encoder_interface.read_encoder_data()
        print(f"MT = {encoder_data[0]}, ST = {encoder_data[1]}°")
        time.sleep(0.1)
