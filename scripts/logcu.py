#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


class Logcu():

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename='./log/sip3a.log',
                            filemode='a')


    def yaz(self, tip, log):
        if tip == "INFO":
            logging.info(log)
        elif tip == "WARNING":
            logging.warning(log)
        elif tip == "ERROR":
            logging.error(log)
        else:
            logging.debug(log)
