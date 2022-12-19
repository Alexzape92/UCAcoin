import requests
import json
import time
import sqlite3

class block:
    def __init__(self, id, n, trans, prev, dif, nonce, time) -> None:
        self.id = id            #id del bloque (profundidad del bloque)
        self.n = n              #número de transacciones en este bloque
        self.trans = trans      #lista de transacciones
        self.prev = prev        #hash del bloque anterior
        self.dif = dif          #dificultad para el nonce del siguiente bloque
        self.nonce = nonce      #nonce del bloque
        self.time = time        #fecha y hora en la que se creó el bloque
    
    def __str__(self) -> str:
        return 'id = {}, n = {}, trans = {}, prev = {}, dif = {}, nonce = {}, tiempo = {}'.format(self.id, self.n, self.trans, self.prev, self.dif, self.nonce, self.time)

def upd_db(nextid, lasthash, block) -> None:
    db = sqlite3.connect('ucacoin.db')

    db.execute("INSERT INTO blockchain VALUES({}, {}, '{}', '{}', {}, {})".format(nextid, block.n, lasthash, block.dif, block.nonce, block.time))
    #Falta insertar también las transacciones en su tabla correspondiente

    db.commit()
    db.close()

def createBlock() -> None:
    while True:
        datajson = requests.get(url='http://localhost:8081/getTrans').text  #pool es la lista en formato Json

        datajson = json.loads(datajson)
        nextid = datajson['nextid']
        lasthash = datajson["lasthash"]
        pool = datajson["transactions"]

        nonce = requests.get(url='http://localhost:8000/getNonce/500000').text
        currentBlock = block(nextid, len(pool), pool, lasthash, 20000, int(nonce), int(time.time()))


createBlock()
