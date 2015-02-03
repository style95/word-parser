#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import os
import sys


def get_english(line):
    english = re.search(r'[\w|\s|-]*=*(\s*(\([1-9]\))*\s*)*([\w|\s]*,*)*', line, re.M | re.I)
    if english:
        return english.group()
    else:
        return


def get_korean(line):
    korean = re.search(r'[ㄱ-ㅣ가-힣|\(|\)],* *.*', line, re.M | re.I)
    if korean:
        return korean.group()
    else:
        return


OUTPUT_DIR = "output"


def generate_output(input_path, file_name):
    f = open(input_path + "/" + file_name)
    target = open(OUTPUT_DIR + "/" + file_name, 'w')
    line = f.readline()
    while 1:
        if not line:
            break
        number = re.search(r'\([1-9]\)', line, re.M | re.I)
        if not number:
            english = get_english(line)
            korean = get_korean(line)
            words = english.split('=')
            keyword = words[0]
            answer = words[1]
            words = words[1].split(', ')
            str_sum = ""
            for word in words:
                str_sum = str_sum + word[0] + ", "
            str_sum = str_sum[:len(str_sum) - 2] + ";"
            first_line = keyword + " = " + str_sum
            second_line = answer
            third_line = korean

            target.write(first_line.rstrip('\n') + '\n')
            target.write(second_line.rstrip('\n') + '\n')
            if third_line is not None:
                target.write(third_line.rstrip('\n') + '\n')
            target.write('\n')
            line = f.readline()
        else:
            num = 1
            number = re.search(r'\(' + str(num) + '\)', line, re.M | re.I)
            english = get_english(line)
            words = english.split('=(' + str(num) + ') ')
            keyword = words[0]

            first_line = keyword + " = "
            second_line = ""
            third_line = ""
            while number:
                korean = get_korean(line)
                korean_num = re.search(r'\([1-9]\)', korean, re.M | re.I)
                if korean_num:
                    korean = korean.split('(' + str(num) + ') ')
                    korean = korean[1]
                    korean = get_korean(korean)
                english = get_english(line)
                words = english.split('=(' + str(num) + ') ')
                answer = words[1]
                words = words[1].split(', ')
                str_sum = ""
                for word in words:
                    str_sum = str_sum + word[0] + ", "
                str_sum = str_sum[:len(str_sum) - 2]
                first_line = first_line + " (" + str(num) + ") " + str_sum
                second_line = second_line + "(" + str(num) + ") " + korean + " " + answer

                num += 1
                line = f.readline()
                if not line:
                    break
                number = re.search(r'\(' + str(num) + '\)', line, re.M | re.I)

            first_line += ";"
            target.write(first_line + '\n')
            target.write(second_line + '\n')
            target.write(third_line + '\n')
    f.close()
    target.close()


if len(sys.argv) == 1:
    print "Please specify the input directory: ./word.py {INPUT_DIR}"
    exit(1)

input_dir = sys.argv[1]
files = os.listdir(input_dir)
try:
    os.stat(OUTPUT_DIR)
except OSError:
    os.mkdir(OUTPUT_DIR)

for input_file in files:
    generate_output(input_dir, input_file)

