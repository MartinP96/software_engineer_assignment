
'''
    File name: main.py
    Version: v0.1
    Date: 23.12.2022
    Desc: Main python script file for software engineer assignment
'''

import time
from encoder_interface import EncoderInterface

if __name__ == '__main__':

    encoder_interface = EncoderInterface('COM8')

    while 1:

        encoder_data = encoder_interface.read_encoder_data()
        print(f"MT = {encoder_data[0]}, ST = {encoder_data[1]}°")
        time.sleep(0.1)
