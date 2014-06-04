#!/usr/bin/env python
# -*- coding: utf-8 -*-

#filename: katip.py

import sys
from xml.dom import minidom
from logcu import Logcu
import hafiye


#sys.path.append("./data")

class Katip(object):

    def __init__(self, kaynakXML="./data/TVGenel.xml"):
        self.kaynakXML = kaynakXML
        self.logcu = Logcu()

        try:
            self.xml_doc = minidom.parse(kaynakXML)
            self.doc_root = self.xml_doc.documentElement
        except IOError, e:
            self.logcu.yaz("ERROR", u"[%s] XML dosyası okunamadı. %s" %(self.kaynakXML, e))
            print u"HATA: [%s] XML dosyası okunamadı. %s" %(self.kaynakXML, e)
        except ExpatError, e:
            self.logcu.yaz("ERROR", u"[%s] XML dosyası parse edilemedi. %s" %(self.kaynakXML, e))
            print u"HATA: Kaynak XML dosyası [%s] parse edilemedi. %s" %(self.kaynakXML, e)
            #TODO:ExpatError yerine minidom hata sınıflarını kullanmak lazım.
        except:
            logcu.yaz("ERROR", u"Katip.__init__() içinde hata oluştu.")
            print u"HATA: Katip.__init__() içinde hata oluştu."

        self.logcu.yaz("INFO", u"[%s] dosyası parse edildi." %self.kaynakXML)
        print "="*50
        print u"BİLGİ: [%s] dosyası parse edildi." %self.kaynakXML

    def kanal_ekle(self, kanaladi, kanalip):
        hfy = hafiye.Hafiye()
        hfy.Parse(self.kaynakXML)
        #kanal_adlari_listesi = hfy.kanal_adlarini_getir()
        kanal_sipleri_listesi = hfy.kanal_siplerini_getir()

        try:
            if kanalip in kanal_sipleri_listesi:
                self.logcu.yaz("WARNING", u"[%s] ip numarası kullanımda." %kanalip)
                self.logcu.yaz("WARNING", u"program sonlandırılacak.")
                print u"UYARI: [%s] ip numarası kullanımda." %kanalip
                print u"UYARI: program sonlandırılacak."
                print "-"*50
                print u"ÖNERİ: Kullanılmayan bir ip numarası belirleyip\nyeniden deneyin."
                print "="*50
                return

            else:
                print u"BİLGİ: [%s] ip numarası kullanımda değil." %kanalip
                node = self.xml_doc.createElement("kanal")
                kanaladi = kanaladi.decode("utf-8")

                element = self.xml_doc.createElement("kanaladi")
                element.appendChild(self.xml_doc.createTextNode(kanaladi))
                node.appendChild(element)

                element = self.xml_doc.createElement("kanalip")
                element.appendChild(self.xml_doc.createTextNode(kanalip))
                node.appendChild(element)
                self.doc_root.appendChild(node)
                file = open(self.kaynakXML,'w')
                file.write(self.xml_doc.toxml("utf-8"))
                #file.write(self.xml_doc.toprettyxml( ))

        #TODO: expaterror yarine bi hata sınıfı bul.
        except ExpatError, e:
            self.logcu.yaz("ERROR", u"%s %s ip no ile eklenirken hata oluştu. %s" %(kanaladi, kanalip, e))
            print u"HATA: %s %s ip no ile eklenirken hata oluştu. %s" %(kanaladi, kanalip, e)
        except IOError, e:
            self.logcu.yaz("ERROR",  u"%s %s ip no ile XML dosyasına yazılamadı. %s" %(kanaladi, kanalip, e))
            print u"HATA: XML dosyasına yazılamadı. %s" %e
        except:
            self.logcu.yaz("ERROR", u"Katip.kanal_ekle() içinde hata oluştu.")
            print u"HATA: Katip.kanal_ekle() içinde hata oluştu."

        self.logcu.yaz("INFO", u"[%s] kanalı [%s] stream-ip si [%s] dosyasına kaydedildi." %(kanaladi, kanalip, self.kaynakXML))
        print u"BİLGİ: [%s] kanalı [%s] stream-ip si [%s] dosyasına kaydedildi." %(kanaladi, kanalip, self.kaynakXML)


    def kanal_sil(self, kanaladi):
        try:
            hits = 0
            kanaladi = kanaladi.decode("utf-8")
            kanallar = self.xml_doc.getElementsByTagName("kanal")

            for kanal in kanallar:
                knl = kanal.childNodes
                for k in knl:
                    if k.nodeName == "kanaladi":
                        if k.firstChild.data.strip( ) == kanaladi:
                            hits = hits + 1
                            self.doc_root.removeChild(kanal)

            if hits > 0:
                file = open(self.kaynakXML,'w')
                file.write(self.xml_doc.toxml("utf-8"))
                self.logcu.yaz("INFO", "[%s] dosyasında [%s] kanalına ait [%0d] adet kayda rastlandı." %(self.kaynakXML, kanaladi, hits))
                self.logcu.yaz("INFO", "[%s] kanalı ait [%s] dosyasından silindi." %(kanaladi, self.kaynakXML))
                print u"BİLGİ: [%s] dosyasında [%s] kanalına ait [%0d] adet kayda rastlandı." %(self.kaynakXML, kanaladi, hits)
                print u"BİLGİ: [%s] kanalı [%s] dosyasından silindi." %(kanaladi,self.kaynakXML)
            else:
                print u"BİLGİ: [%s] kanalına [%s] dosyasında rastlanmadı." %(kanaladi, self.kaynakXML)
        #TODO: expaterror yarine bi hata sınıfı bul.
        except Exception, e:
            self.logcu.yaz("ERROR", u"[%s] kanalı silinirken hata oluştu. %s" %(kanaladi, e))
            print u"HATA: Kanal silinirken hata oluştu. %s" %e
        except IOError, e:
            self.logcu.yaz("ERROR",  u"Katip.kanal_sil() XML dosyasına yazılamadı. %s" %e)
            print u"HATA: XML dosyasına yazılamadı. %s" %e
        except:
            self.logcu.yaz("ERROR", u"Katip.kanal_sil() içinde hata oluştu.")
            print u"HATA: Katip.kanal_sil() içinde hata oluştu."
