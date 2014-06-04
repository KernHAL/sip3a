#!/usr/bin/env python
# -*- coding: utf-8 -*-

#filename: izci.py

import os


def iz_sur(hedef):
    komut_bul = "./sip3a --list std | grep --color -i %s" %hedef  # hit leri buluyor.
    komut_say = "./sip3a --list std | grep -c -i %s" %hedef  # hit leri sayıyoruz.

    print "="*40
    os.system(komut_bul)
    sonuc = os.popen(komut_say)
    hit = sonuc.readline().strip()
    sonuc.close()

    print "="*40
    print u"BİLGİ: [%s] adet eşleşme bulundu." %hit
