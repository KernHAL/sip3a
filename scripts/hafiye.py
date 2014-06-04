#!/usr/bin/env python
# -*- coding: utf-8 -*-

#filename: hafiye.py

from xml.parsers import expat


class Hafiye(object):

    def __init__(self):
        self.etkinDugum = ""
        self.dugumSayisi = 0
        self.kanalAdi = ""
        self.kanalIP = ""
        self.kanallar = {}


    def StartElement(self, name, attributes):
        if name == "kanaladi":
            self.etkinDugum = "kadi"
        elif name == "kanalip":
            self.etkinDugum = "kip"
        else:
            self.tag = "kanal"


    def EndElement(self, name):
        if name == "kanal":
            self.kanallar[self.kanalAdi] = self.kanalIP
            self.dugumSayisi +=1


    def CharacterData(self, data):
        if data.strip():
            data = data.encode("utf-8")
            if self.etkinDugum == "kadi":
                self.kanalAdi = data.strip()
            elif self.etkinDugum == "kip":
                self.kanalIP = data.strip()


    def Parse(self, fName):
        xmlParser = expat.ParserCreate()
        xmlParser.StartElementHandler = self.StartElement
        xmlParser.EndElementHandler = self.EndElement
        xmlParser.CharacterDataHandler = self.CharacterData
        xmlParser.Parse(open(fName).read(), 1)


    def listele(self, olcu):
        kanallar = self.kanallar

        def swapDict(kanallar):
            knl = {}
            for kadi, kip in kanallar.iteritems( ):
                knl[kip]=kadi
            return knl

        def sortDict(kanallar):
            sirali = {}
            keys = kanallar.keys( )
            keys.sort( )
            for key in keys:
                sirali[key] = kanallar[key]
            return sirali

        if olcu == "ip":
            kanallar = swapDict(kanallar)
            kanaladlari = kanallar.keys( )
            kanaladlari.sort( )
            print '='*40
            print "KANAL IP".ljust(27), "KANAL ADI".center(13)
            print '='*40
            for kanaladi in kanaladlari:
                print kanaladi.ljust(27, '.'), kanallar[kanaladi]
            print '='*40
            print "BILGI: %04d adet kanal listelendi." % self.dugumSayisi
        elif olcu == "kadi":
            kanaladlari = kanallar.keys( )
            kanaladlari.sort( )
            print '='*40
            print "KANAL ADI".ljust(27), "KANAL IP".center(13)
            print '='*40
            for kanaladi in kanaladlari:
                print kanaladi.ljust(27, '.'), kanallar[kanaladi]
            print '='*40
            print "BILGI: %04d adet kanal listelendi." % self.dugumSayisi
        else:
            print '='*40
            print "KANAL ADI".ljust(27), "KANAL IP".center(13)
            print '='*40
            for kanaladi, kanalip in kanallar.iteritems( ):
                print kanaladi.ljust(27, '.'), kanalip
            print '='*40
            print "BİLGİ: %04d adet kanal listelendi." % self.dugumSayisi


    def kanal_adlarini_getir(self):
        kanal_adlari = self.kanallar.keys()
        return kanal_adlari


    def kanal_siplerini_getir(self):
        kanal_sipleri = self .kanallar.values()
        return kanal_sipleri
