from copyreg import pickle
import random
import time
import pickle
import os
import re

import conf




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


def challenge():
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())
    with open(conf.MOD_PATH, "rb") as f:
        modified_files = pickle.load(f)
    numero1 = random.randint(0,10)
    numero2 = random.randint(0,10)
    error_auth = 0
    x = random.random()
    log(local_time + " Authentication challenge Starting")
    if x>0.5:
        res = numero1+numero2
        resP = int(input("Resuelve "+ str(numero1) +" + "+str(numero2)+": "))
        if res==resP:
            print('Eres humano!')
            exec(open(os.path.join(conf.PATH,"genBD.py")).read())
        else:
            print('Eres un robot!')
            globals()['humano'] = False
            #for new_file in new_files:
                #log(local_time + " [error_auth] "  + new_file + " se ha intentado añadir a la base de datos")
            for modified_file in modified_files:
                log(local_time + " [error_auth] "  + modified_file + " se ha intentado modificar")
                error_auth = error_auth + 1
        
    else:
        res = numero1-numero2
        resP = int(input("Resuelve "+ str(numero1) +" - "+str(numero2)+": "))
        if res==resP:
            print("¡Eres humano!")
            exec(open(os.path.join(conf.PATH,"genBD.py")).read())
        else:
            print("¡Eres un robot!")
            globals()['humano'] = False

            #if new_files:
                #for new_file in new_files:
                    #log(local_time + " [error_auth] "  + new_file + " se ha intentado añadir a la base de datos")
                    #globals()['error_auth'] = globals()['error_auth'] + 1
            if modified_files:
                for modified_file in modified_files:
                    log(local_time + " [error_auth] "  + modified_file + " se ha intentado modificar")
                    error_auth = error_auth + 1
    log(local_time + " Auth_Error(s) : " + str(error_auth))
    log(local_time + " Authentication challenge Finished")

if __name__ == "__main__":

    humano = True
    
    
    
    log_file = None
    try:
        log_file = open(conf.LOGS, "a")
    except Exception as e:
        print("Algo no esta funcionando como debería al abrir el log: " + str(e))
        exit(0)

    print("¿Eres humano? \n Debes resolver la siguiente prueba: ")
    challenge()
    

    if log_file is not None:
        log_file.close()
    

    


