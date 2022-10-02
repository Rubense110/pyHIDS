#!/usr/bin/env python3

import pickle
import time
import hashlib
import os

import conf


#Carga de la base de datos
def load_base():
    """
    Carga el base file.

    Devuelve un diccionario con la ruta (file name) y el hash del file.
    """
    database = None
    with open(conf.BASE_PATH, "rb") as serialized_database:
        database = pickle.load(serialized_database)
    
    return database

#Escritura en log

def log(message, display=False):
    """
    Devuelve por consola y escribe el log en el log file.
    """
    
    if display:
        print(message)
    try:
        log_file.write(message+"\n")
    except Exception as e:
        print(e)
        
def compare_hash(target_file, expected_hash):
    """
    Comparamos 2 valores hash.

    Comparamos el hash del fichero seleccionado y el hash que esperamos obtener,
    el que hemos almacenado en la base de datos.
    """
    sha256_hash = hashlib.sha256()
    opened_file = None
    comp = True

    # cada log contiene la fecha y hora de la incidencia
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

    # comprobamos por seguridad que el hash esperado no está vacio
    if expected_hash == "":
        globals()['warning'] = globals()['warning'] + 1
        log(local_time + " No hash value for " + target_file)

    # abrimos el contenido del fichero seleccionado para comenzar con el test
    try:
        opened_file = open(target_file, "rb")
        data = opened_file.read()
    except:
        globals()['error'] = globals()['error'] + 1
        log(local_time + " [error] " + \
                   target_file + " no existe. " + \
                  "o no tienes el suficiente privilegio para leerlo.")
    finally:
        if opened_file is not None:
            opened_file.close()

    # comenzazmos con la comparación de hashs
    if opened_file is not None:
        sha256_hash.update(data)
        hashed_data = sha256_hash.hexdigest()

        if hashed_data == expected_hash:
            # todo está correcto, sólo escribimos la fecha de la comprobación y que el fichero no ha sido modificado
            log(local_time + " [notice] "  + target_file + " ok")
        else:
            # ha sido modificado, warning
            # reportamos la alerta en el log file
            globals()['warning'] = globals()['warning'] + 1
            message = local_time + " [warning] " + target_file + " ha sido modificado."
            # pyHIDS log, escribimos en el fichero y mostramos por pantalla la incidencia
            log(message, True)

            return False
    
    return comp

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


def detectionNewFiles():
    res = []
    #Recogemos todos los ficheros que han sido añadidos al conjunto de ficheros global (ficheros)
    for rules in conf.FOLDER_FILES:
        new_files = search_files(rules[0], rules[1])

    if os.path.exists(conf.BASE_PATH):
        with open(conf.BASE_PATH,"rb") as r:
            older_database = pickle.load(r)
        for file in new_files:
            if file not in list(older_database.keys()):
                res.append(file)
    return res
            



if __name__ == '__main__':
    files_modified = []
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())
    #Abrimos el fichero de log
    log_file = None
    try:
        log_file = open(conf.LOGS, "a")
    except Exception as e:
        print("Algo no esta funcionando como debería al abrir el log: " + str(e))
        exit(0)
    
    log(time.strftime("[%d/%m/%y %H:%M:%S] HIDS starting.", \
                           time.localtime()))

    warning, error = 0, 0

    # hacemos efectiva la carga de la base de datos, con la ruta de los ficheros y sus hashs.
    base = load_base()
    if base is None:
        print("La base de hashes no ha podido ser cargada.")
        #si no se ha podido cargar finalizamos el programa
        exit(0)

    #Comprobamos la integridad de los ficheros

    for file in list(base.keys()):
        if os.path.exists(file):
            t = compare_hash(file, base[file])
            #apilamos los ficheros que han sufrido cambios, ya que t devuelve true en caso de tener mismo hash
            if not t:
                files_modified.append(file)
        else:
            error = error + 1
            log(local_time + " [error] " + \
                   file + " no existe, o no tienes el suficiente privilegio para leerlo.", True)
    
    new_files = detectionNewFiles()

    if new_files:
        for new_file in new_files:
            message = local_time + " [warning] "  + new_file + " ha sido agregado"
            log(message,True)
            warning = warning + 1

    #Finalizamos 
    
    log(local_time + " Error(s) : " + str(error))
    log(local_time + " Warning(s) : " + str(warning))
    log(local_time + " HIDS finished.")

    if log_file is not None:
        log_file.close()
    if files_modified:
        with open(conf.MOD_PATH,"wb") as f:
            pickle.dump(files_modified,f)