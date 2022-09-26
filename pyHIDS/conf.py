import os

PATH = os.path.abspath(".")
BASE_PATH = os.path.join(PATH,"base","database.pickle")
MOD_PATH = os.path.join(PATH,"base","files_mod.pickle")
NEW_PATH = os.path.join(PATH,"base","new_files.pickle")

#Archivos especificos a escanear
SPECIFIC_FILES_TO_SCAN = [os.path.join(PATH,"decisiones.txt")]

#Carpetas y patrón
FOLDER_FILES = [(".*",os.path.join(PATH,"ficheros"))]

#Donde almacenar el log
LOGS = os.path.join(PATH,"logs", "log")
