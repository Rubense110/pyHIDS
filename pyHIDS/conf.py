#!/usr/bin/env python3

import os

PATH = os.path.abspath(".")
BASE_PATH = os.path.join(PATH,"base","database.pickle")
MOD_PATH = os.path.join(PATH,"base","files_mod.pickle")

#Archivos especificos a escanear
SPECIFIC_FILES_TO_SCAN = [os.path.join(PATH,"conf.py"),os.path.join(PATH,"genBD.py"),
                        os.path.join(PATH,"lanzador.py"),os.path.join(PATH,"pyHIDS.py"),
                        os.path.join(PATH,"randomChallenge.py"),os.path.join(PATH,"revisiones.py"),
                        os.path.join(PATH,"lanzador.exe"),os.path.join(PATH,"revisiones.exe"),os.path.join(PATH,"pyHIDS.py")]

#Carpetas y patrón
FOLDER_FILES = [(".*",os.path.join(PATH,"ficheros"))]

#Dónde almacenar el log
LOGS = os.path.join(PATH,"logs", "log.txt")

#Tarea TaskScheduler (Windows) Revisión
TASKSC = "SCHTASKS /CREATE /SC DAILY /TN HIDS\RevisionTask /TR " +os.path.join(PATH,"pyHIDS.exe")+" /ST "
TASKRESUMW = "SCHTASKS /CREATE /SC MONTHLY /D 1 /TN HIDS\ResumenTask /TR " +os.path.join(PATH,"revisiones.exe")+" /ST 00:00"

#Tarea CromTab (Linux) Revisión
TASKCR = "crontab -e 0 11 * * * "+os.path.join(PATH,"pyHIDS.py")
TASKRESUML= "crontab -e 0 0 1 * * "+os.path.join(PATH,"revisiones.py")







