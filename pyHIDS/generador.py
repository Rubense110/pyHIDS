import os
import random

import conf

i = 0
while i<10000:
    x = random.random()

    if x>0.5:
        with open(os.path.join(conf.PATH,"base_datos","txt","File"+str(i)+".txt"),"w") as f:
            f.write("no corrupto")
            f.close()
    else:
        with open(os.path.join(conf.PATH,"base_datos","documentos","File"+str(i)+".doc"),"w") as f:
            f.write("no corrupto")
            f.close()
    i+=1


