import hashlib
import random
from datetime import datetime
import EstructuraBC
import algorithms  
globals = EstructuraBC.globals


def searchNonce(diff) -> int:   #Esto recibe el hash del bloque y buscará el nonce
    encontrado = False
    while not encontrado:
        nonce = random.randint(0, 99999)    #probamos con este nonce
        tempBlock = EstructuraBC.block(globals.newxtid, globals.pool.__len__(), globals.pool, globals.lasthash
        , diff, nonce, datetime.now())  #El bloque que estamos intentando generar

        if hash(hashlib.sha256(str(tempBlock))) < diff:
            encontrado = True
            return nonce