#!/usr/bin/env python3
from PIL import Image
import cv2
import pytesseract
import argparse
import os
from guesslang import Guess
import re
import sys

# Fix indentation and common OCR mistakes
# This is just (barely) enough to handle the example 'helloworld.png' image
def fix_python_code(code):
    result = ''
    indentation = 0
    for line in code.split('\n'):
        result += '    '*indentation + line + '\n'
        if re.search('^(if|for|def)\s', line):
            indentation += 1
        elif re.match('^\s*$', line):
            if indentation > 0:
                indentation -= 1
    result = result.replace('”', '"')
    result = result.replace('o', 'o')       
    return result

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True)
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename),
        config="-psm 4 -c preserve_interword_spaces=1,tessedit_char_whitelist=\"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.-;:_!#%&/()=?`@${[]}\\+\\\'\\\" \"")
    os.remove(filename)

    language = Guess().language_name(text)
    if language != 'Python':
        print('Unknown programming language')
        sys.exit()

    code = fix_python_code(text)

    print('--------------------')
    print("Output:")
    print('--------------------')
    exec(code)
    print('--------------------')

    
