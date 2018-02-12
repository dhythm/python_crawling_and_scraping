import sys
import os
import base64

def main():

    argc = len(sys.argv)

    if (argc != 2):
        print('Usage: $ python %s encode_str' % sys.argv[0])
        quit()

    base64string = base64.b64encode(sys.argv[1].encode('utf-8')).decode('utf-8')
    print(base64string)

if __name__ == '__main__':
    main()

