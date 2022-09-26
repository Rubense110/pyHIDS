import os

import conf


if __name__ == '__main__':
    print("Bienvenido al entorno de configuración de HIDS INSEGUS")

    #Comprobamos si el fichero donde almacenamos la base de datos existe mediante su path
    if not os.path.exists(conf.BASE_PATH):
        print("Aún no ha sido generada la base de datos de seguridad...")
        gen_base = input("Generar base de datos [y/n]: ")
        if gen_base=="y":
            exec(open(os.path.join(conf.PATH,"genBD.py")).read())
    

    print("\nOpción 1: Establecer periodo de revisión")
    print("Opción 2: Realizar revisión")
    print("Opción 3: Salir de entorno de configuración")

    case = int(input("Escoja opción: "))
    
    while case >3 or case==0:
        case = int(input("Debe escoger entre [1 | 2 | 3], escoja opción: "))
        
    if case==1:
        print("k")
        exit(0)
    elif case==2:
        print("Realizando revisión...")
        exec(open(os.path.join(conf.PATH,"pyHIDS.py")).read())
        print(""+"\nRevisión finalizada")
        case2 = input("¿Desea actualizar la base de datos existente? [y/n]: ")
        if case2 == "y":
            case3 = input("Si algún fichero ha sufrido una modificación en su integridad podrían estar en peligro"+ \
                                "\nla información almacenada en ellos, ¿está seguro de actualizar la base de datos? [y/n]: ")                  
            if case3=="y":
                #Iniciamos el Hand-Shake Protocol
                exec(open(os.path.join(conf.PATH,"randomChallenge.py")).read()) 
            
            else:
                print("Saliendo..")
                exit(0)
        else:
            print("Saliendo..")
            exit(0)
    elif case==3:
        print("Saliendo..")
        exit(0)