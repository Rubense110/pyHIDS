import os

PATH = os.path.abspath(".")
BASE_PATH = os.path.join(PATH,"base","database.pickle")

#Archivos especificos a escanear
SPECIFIC_FILES_TO_SCAN = [os.path.join(PATH,"decisiones.txt")]

#Carpetas y patrón
FOLDER_FILES = [(".*",os.path.join(PATH,"ficheros"))]

#Donde almacenar el log
LOGS = os.path.join(PATH,"logs", "log")
