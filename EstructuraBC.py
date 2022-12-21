from __future__ import annotations
import time
import json
import sqlite3
from bottle import get, run, post, request

class globals:
    pool = list()   #lista de transacciones
    newxtid = -1     #id del siguiente bloque a crear
    lasthash = 0

class transaction:
    def __init__(self, usero, userd, cant, date) -> None:
        self.usero = usero      #id del usuario que realiza la transacción
        self.userd = userd      #id del usuario que recibe la transacción
        self.cant = cant        #cantidad de criptomonedas transferidas
        self.date = date
    
    def __str__(self) -> str:
        return "sender: {}, receiver: {}, amount: {}".format(self.usero, self.userd, self.cant)

class user:
    def __init__(self, id, key, wallet) -> None:
        self.id = id            #id del usuario  
        self.key = key          #clave del usario (hash)
        self.quant = wallet    #cantidad de criptomonedas del usuario
    
    def __str__(self) -> str:
        return "{}, {}, {}".format(self.id, self.key, self.quant)
    
    def get_obj_us(id) -> user: #Este método accede a la base de datos de los usuarios y devueve el objeto user parseado
        db = sqlite3.connect('ucacoin.db')
        cur = db.cursor()

        cursor = cur.execute("SELECT * FROM Wallets WHERE Id = '{}'".format(id))
        result = cursor.fetchall()

        for row in result:
            db.close()
            return user(row[0], row[1], row[2])
    
    #Comprueba que el usuario tenga la contraseña especificada (Habrá que hashearla en futuras versiones)
    def check_user(id, key) -> bool:
        us = user.get_obj_us(id)     
    
        return (us.key == key)
    
    #Comprueba que el usuario que realiza una transacción tenga suficientes UCACoins
    def check_quant(id, quant) -> bool:
        us = user.get_obj_us(id)

        return (us.quant >= quant)
    
    #Actualiza las carteras de los usuarios
    def act_quant(id1, id2, q) -> None:
        db = sqlite3.connect('ucacoin.db')

        db.execute("UPDATE Wallets SET Amount = Amount - {} WHERE Id = '{}'".format(q, id1))
        db.execute("UPDATE Wallets SET Amount = Amount + {} WHERE Id = '{}'".format(q, id2))

        db.commit()
        db.close()


def register(id, passwd) -> None:   #Este método registra un usuario en la base de datos con la id pasada
    return                          #y la contraseña (sin cifrar), por lo que antes hay que hashearla

@post('/Transfer')
def transfer():     #solicitar una transacción
    datajson = request.json

    origin = datajson['origin']
    key = datajson['key']
    dest = datajson['dest']
    quant = datajson['quant']
    date = int(time.time())

    #COMPROBAR QUE LA TRANSACCIÓN ES VALIDA
    if(user.check_user(origin, key) == False):
        raise Exception('CLAVE')
    if(user.check_quant(origin, quant) == False):
        raise Exception('CANTIDAD')

    #A partir de aquí la transacción está validada, actualicemos los usuarios
    user.act_quant(origin, dest, quant)

    trans = transaction(origin, dest, quant, date)    #Creamos el objeto transacción y lo guardamos en el pool
    globals.pool.append(trans)

@get('/getTrans')
def transactions():
    list_act = list()

    for trans in globals.pool:
        tempdict = {"usero": trans.usero, "userd": trans.userd, "cant": trans.cant, "date": trans.date}
        list_act.append(tempdict)
    
    if globals.newxtid == -1:
        db = sqlite3.connect('ucacoin.db')
        cur = db.cursor()

        cur = cur.execute("SELECT * FROM blockchain")
        result = cur.fetchall()

        #Guardamos en el campo nextid la última id que se ha encontrado en la BD (si está vacía sigue siendo -1)
        for row in result:
            globals.newxtid = row[0]

        
        db.close()
        
        #Le sumamos una para que no se repita
        globals.newxtid = globals.newxtid + 1
    
    json_act = json.dumps({"nextid":globals.newxtid, "lasthash": globals.lasthash, "transactions": list_act})

    return json_act

@post('/actGlobals')
def act():
    datajson = request.json

    myhash = datajson['hash']
    n = datajson['n']
    globals.newxtid = globals.newxtid + 1
    globals.lasthash = myhash

    i = 0
    while i < n:
        globals.pool.pop(0)
        i = i+1

if __name__ == '__main__':
    run(host='localhost', port=8081)