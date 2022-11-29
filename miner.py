import hashlib
import random
import time
import EstructuraBC
import algorithms  
from bottle import get, run
globals = EstructuraBC.globals

@get('/getnonce/<diff>')
def searchNonce(diff) -> int:   #Esto recibe el hash del bloque y buscará el nonce
    encontrado = False
    nonce = 0
    while not encontrado:
        print("posible nonce: " + str(nonce))
        tempBlock = EstructuraBC.block(globals.newxtid, globals.pool.__len__(), globals.pool, globals.lasthash
        , diff, nonce, time.time())  #El bloque que estamos intentando generar

        #print("Hash obtenido: " + str(int(hashlib.sha256(str(tempBlock).encode('utf-8')).hexdigest(), 16) % pow(10,19)))
        #print("Dificultad: " + diff)

        if int(hashlib.sha256(str(tempBlock).encode('utf-8')).hexdigest(), 16) % pow(10, 12) < int(diff):
            encontrado = True
            return str(nonce)
        
        nonce = nonce + 1

run(host='localhost', port=8000)