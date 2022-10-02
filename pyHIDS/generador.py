import os
import random

import conf

i = 1
while i<900:
    x = random.random()

    if x>0.5:
        with open(os.path.join(conf.PATH,"ficheros","txt","File"+str(i)+".txt"),"w") as f:
            f.write("no corrupto")
            f.close()
    else:
        with open(os.path.join(conf.PATH,"ficheros","documentos","File"+str(i)+".doc"),"w") as f:
            f.write("no corrupto")
            f.close()
    i+=1


