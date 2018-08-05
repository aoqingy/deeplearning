#!/usr/bin/python
#-*- coding: UTF-8 -*-
import os
import logging
import logging.handlers

BASE_DIR = os.path.dirname(__file__)

logger = logging.getLogger("logisticr")
#hdlr = logging.FileHandler(os.path.join(BASE_DIR, "Logistic.log"))
hdlr = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(BASE_DIR, "logs", "logistic.log"),  when='midnight', backupCount=7)
#hdlr.suffix = "%Y%m%d.log"	#如果加入这行就不会删除历史日志，因为删除文件名匹配失败
#formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
formatter = logging.Formatter('[%(asctime)s] {%(filename)-10s:%(lineno)-4d} %(levelname)-5s - %(message)s','%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

