#!/usr/bin/env python3
from importlib.metadata import files
import pickle
import os
import hashlib


import conf



def search_files(motif, root_path):
    """
    Devuelve una lista de ficheros.

    Busca todos los ficheros que contengan
    como extension 'motif' y que no sean accesos directos.
    """
    result = []
    #Realiza una revisión en profundidad del contenido de la base de ficheros. Todos estos y el contenido de las subcarpetas
    w = os.walk(root_path)
    import re
    for (path, dirs, files) in w:
        for f in files:
            if re.compile(motif).search(f):
                # if not a symbolic link
                if not os.path.islink(os.path.join(path, f)):
                    result.append(os.path.join(path, f))
    return result


def hash_file(target_file):
    """
    Hace el hash del fichero en concreto.
    """
    sha256_hash = hashlib.sha256()
    opened_file = None
    hashed_data = None
    data = None

    # Posibles errores al abrir el log
    try:
        opened_file = open(target_file, "rb")
        data = opened_file.read()
    except Exception as e:
        # Si el file no existe, lo eliminamos de la lista a analizar
        print(target_file, ":", e)
        globals()['number_of_files_to_scan'] = \
            globals()['number_of_files_to_scan'] - 1
        del list_of_files[list_of_files.index(target_file)]
    finally:
        if data is not None:
            opened_file.close()

    if data is not None:
        sha256_hash.update(data)
        hashed_data = sha256_hash.hexdigest()

    return hashed_data




if __name__ == '__main__':
    database = {}
    list_of_files = conf.SPECIFIC_FILES_TO_SCAN

    for rules in conf.FOLDER_FILES:
        #Añadimos a la lista de ficheros todos los que se encuentren en el folder (rule[1])
        # y que cumplan con la extensión/patrón (rule[0])
        list_of_files.extend(search_files(rules[0], rules[1]))
    number_of_files_to_scan = len(list_of_files)

    print("Generating database...")

    for file in list_of_files:
        hashed_file = hash_file(file)
        if hashed_file is not None:
            database[file] = hashed_file

    #Serializamos el database

    with open(conf.BASE_PATH,"wb") as f:
        pickle.dump(database,f)
    
    print(number_of_files_to_scan, "files in the database.")