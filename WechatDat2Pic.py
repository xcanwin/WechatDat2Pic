#!/usr/bin/env python
# -- coding: utf-8 --

# By default, wechat dat files are in "xxx:\\Documents\\WeChat Files\\xxx\\Data\\", and temporary dat files are in "xxx:\\Documents\\WeChat Files\\xxx\\Data\\Tiny\\"

import os, sys, binascii

def decodeDat(fn):
    read = open(fn, 'rb').read()
    hexfile = binascii.b2a_hex(read)
    obj = []
    headerhex1 = int(hexfile[0:2], 16)
    headerhex2 = int(hexfile[2:4], 16)
    hs = [('jpg', 0xff, 0xd8), ('png', 0x89, 0x50), ('bmp', 0x42, 0x4d), ('gif', 0x47, 0x49)]
    k = ''
    for filetype, h1, h2 in hs:
        if hex(headerhex1 ^ h1) == hex(headerhex2 ^ h2):
            k = h1
            break
    if k == '':
        print '[-] error:', fn
    else:
        for i in xrange(0,len(hexfile),2):
            h = int(hexfile[i:i+2], 16)
            hnew = ( k ^ int(hexfile[0:2], 16) ) ^ h
            hnew = hex(hnew)[2:]
            if len(hnew) == 1:
                hnew = '0' + hnew
            obj.append(hnew)
        binfile = binascii.a2b_hex(''.join(obj))
        fnnew = fn + '.' + filetype
        open(fnnew, 'wb').write(binfile)
        print '[+] save as:', fnnew

if len(sys.argv)<2:
    print 'usage: python', sys.argv[0], '[DATFILE]'
    print 'usage: python', sys.argv[0], '[DATPATH]'
else:
    fn = sys.argv[1]
    if os.path.exists(fn):
        if os.path.isfile(fn):
            decodeDat(fn)
        elif os.path.isdir(fn):
            for fnTmp in os.listdir(fn):
                decodeDat(fn + '\\' + fnTmp)
