sip3a nedir?
=====================================================

sip3a programını RTÜK bünyesinde geliştirilen SKAAS projesi kapsamında takibi
öngörülen tv ve rd kanallarına verilen stream-ip lerinin takibini, yenilerinin
eklenmesini, mevcut olanlarının değiştirilmesini veya silinmesini ve ardından
yapılan bütün değişikliklerin ilgili tüm sunuculara dağıtılmasını sağlamak
için geliştirildim.

Aşağıda sip3a nın değişik kullanımlarını veriyorum:

Kanal sorgulama:

            sip3a --search='KANAL 1'

Kanalları listeleme:

            sip3a --list
            sip3a --list=kadi
            sip3a --list=ip

Kanal ekleme:

            sip3a --add='DISCOVERY CHANNEL' 239.1.1.40

Kanal çıkarma:

            sip3a --remove='DISCOVERY CHANNEL'

Kanal listesini dağıtma:

            sip3a --deliver=tv
            sip3a --deliver=rd


mailto: ieser@rtuk.org.tr
