import os

PATH = os.path.abspath(".")
BASE_PATH = os.path.join(PATH,"base","database.pickle")
MOD_PATH = os.path.join(PATH,"base","files_mod.pickle")

#Archivos especificos a escanear
SPECIFIC_FILES_TO_SCAN = [os.path.join(PATH,"decisiones.txt")]

#Carpetas y patrón
FOLDER_FILES = [(".*",os.path.join(PATH,"ficheros"))]

#Donde almacenar el log
LOGS = os.path.join(PATH,"logs", "log.txt")

#Tarea TaskScheduler (windows) Revision
TASKSC = "SCHTASKS /CREATE /SC DAILY /TN HIDS\RevisionTask /TR " +os.path.join(PATH,"pyHIDS.exe")+" /ST "
TASKRESUMW = "SCHTASKS /CREATE /SC MONTHLY /D 1 /TN HIDS\ResumenTask /TR " +os.path.join(PATH,"revisiones.exe")+" /ST 00:00"

#Tarea CromTab
TASKCR = "crontab -e 0 11 * * * "+os.path.join(PATH,"pyHIDS.py")
TASKRESUML= "crontab -e 0 0 1 * * "+os.path.join(PATH,"revisiones.py")






