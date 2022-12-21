import requests
import json
import time
import sqlite3
import hashlib

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

class transaction:
    def __init__(self, usero, userd, cant, date) -> None:
        self.usero = usero      #id del usuario que realiza la transacción
        self.userd = userd      #id del usuario que recibe la transacción
        self.cant = cant        #cantidad de criptomonedas transferidas
        self.date = date
    
    def __str__(self) -> str:
        return "sender: {}, receiver: {}, amount: {}".format(self.usero, self.userd, self.cant)

def upd_db(nextid, lasthash, block) -> None:
    db = sqlite3.connect('ucacoin.db')

    db.execute("INSERT INTO blockchain VALUES({}, {}, '{}', '{}', {}, {})".format(nextid, block.n, lasthash, block.dif, block.nonce, block.time))
    for trans in block.trans:
        db.execute("INSERT INTO Transactions VALUES(NULL, {}, '{}', '{}', {}, {})".format(block.id, trans['usero'], trans['userd'], trans['cant'], trans['date']))

    db.commit()
    db.close()

def createBlock() -> None:
    while True:
        datajson = requests.get(url='http://localhost:8081/getTrans').text  #pool es la lista en formato Json

        datajson = json.loads(datajson)
        nextid = datajson['nextid']
        lasthash = datajson["lasthash"]
        pool = datajson["transactions"]
        diff = 500000

        nonce = requests.get(url='http://localhost:8000/getNonce/{}'.format(diff)).text
        currentBlock = block(nextid, len(pool), pool, lasthash, diff, int(nonce), int(time.time()))

        upd_db(nextid, lasthash, currentBlock)

        myjson = {"hash": hashlib.sha256(str(currentBlock).encode('utf-8')).hexdigest(), "n": len(pool)}
        requests.post(url='http://localhost:8081/actGlobals', json=myjson)


createBlock()
