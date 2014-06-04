#!/usr/bin/env python
# -*- coding: utf-8 -*-

#filename: ulak.py

import subprocess
import os
import time
import sys
import threading

from xml.parsers import expat


class Ulak(threading.Thread):

    sonuclar = {}
    mutex = threading.Lock()

    def __init__ (self,hedef, hedef_grup):
        threading.Thread.__init__(self)
        self.hedef = hedef
        self.hedef_grup = hedef_grup

    def run(self):
        if self.hedef_grup == "tv":
            komut = os.popen("scp ./data/TVGenel.xml root@%s:/opt/skaas/config/" %(self.hedef))
        else:
            komut = os.popen("scp ./data/RDGenel.xml root@%s:/opt/skaas/config/" %(self.hedef))
#TODO: scp nin switch lerini arastir.

#        komut = os.popen("scp ./data/TVGenel.xml root@%s:/opt/skaas/config/" %(self.hedef))
#        komut = os.popen("ping -c 1 %s" %(self.hedef))
#        komut = os.popen("ls /home/eser/")
#        komut = os.popen("df -h | grep /dev/sda")
#        komut = os.popen("free -m")
#        komut = os.popen("df -h | grep /dev/sda")

        sonuc = komut.readlines()
        komut.close()
        Ulak.mutex.acquire()
        Ulak.sonuclar[self.hedef] = sonuc
        Ulak.mutex.release()

#TODO: cfg_oku isimli bir sinif ile hedef sunucular xml dosyasindan alinacak.

class Hedefler(object):

    def __init__(self, hedef_grup="tv"):
        self.hedefler_listesi = []
        self.etkin_grup = ""
        self.hedef_grup = hedef_grup
        self.grup_icinde = False
        self.hedef = ""

    def StartElement(self, name, attributes):
        self.node_tipi = name
        self.node_attr = attributes  # attributes {'adi', 'tv'}

        if self.node_tipi == "grup":
            self.etkin_grup = self.node_attr["id"]
            if self.etkin_grup == self.hedef_grup:
                self.grup_icinde = True
            else:
                self.grup_icinde = False

    def EndElement(self, name):
        if self.node_tipi == "sadi" and self.grup_icinde:
            self.hedefler_listesi.append(self.hedef)

    def CharacterData(self, data):
        #data = data.encode("utf-8")
        if self.grup_icinde:
            if self.node_tipi == "sadi":
                self.hedef = data.strip()

    def Parse(self, fName):
        xmlParser = expat.ParserCreate()
        xmlParser.StartElementHandler = self.StartElement
        xmlParser.EndElementHandler = self.EndElement
        xmlParser.CharacterDataHandler = self.CharacterData
        xmlParser.Parse(open(fName).read(), 1)

    def get_hedefler(self):
        return self.hedefler_listesi


def dagit(hedef_grup):
    ulak_listesi = []
    cfg_file = "./cfg/hedefler.xml"

    hedefler = Hedefler(hedef_grup)
    hedefler.Parse(cfg_file)

    hedef_listesi = hedefler.get_hedefler()

    for hedef in hedef_listesi:
        ulak = Ulak(hedef, hedef_grup)
        ulak.start()
        ulak_listesi.append(ulak)

    for ulak in ulak_listesi:
        ulak.join()

    hosts = Ulak.sonuclar.keys()
    hosts.sort()

    for host in hosts:
        print "[ %s ] --> %s." %(host,Ulak.sonuclar[host])
    print time.ctime()


if __name__ == "__main__":
    ulaklar_listesi = []
    cfg_file = "./cfg/hedefler.xml"

    h = Hedefler("tv")
    h.Parse(cfg_file)

    for hedef in h.hedefler_listesi:
        ulak = Ulak(hedef)
        ulak.start()
        ulaklar_listesi.append(ulak)

    for ulak in ulaklar_listesi:
        ulak.join()

    hosts = Ulak.sonuclar.keys()
    hosts.sort()

    for host in hosts:
        print "[ %s ] --> %s." %(host,Ulak.sonuclar[host])
    print time.ctime()
