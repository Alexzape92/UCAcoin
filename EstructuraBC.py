from __future__ import annotations
import time
import json
import sqlite3
import hashlib
import random
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

@get('/Register')
def register() -> None:             #Este método registra una cartera en la base de datos con el id pasado
    datajson = request.json

    username = datajson['username']
    wallet_id = hashlib.sha256(username.encode('utf-8')).hexdigest()    #id de la cartera asociada al usuario
    random_int = random.randint(0, 10000000)
    wallet_key = hashlib.sha256(str(random_int).encode('utf-8')).hexdigest()

    db = sqlite3.connect('ucacoin.db')
    cur = db.cursor()

    cursor = cur.execute("SELECT * FROM Wallets WHERE Id = '{}'".format(wallet_id))
    result = cursor.fetchall()

    for row in result:
        db.close()
        return {"Code": 403, "description": "That user already has an associated wallet"}

    db.execute("INSERT INTO wallets VALUES('{}', '{}', 0.0)".format(wallet_id, wallet_key))
    db.commit()
    db.close()

    return {"Code": 201, "private_key": wallet_key}

@post('/Transfer')
def transfer():     #solicitar una transacción
    datajson = request.json

    #el id de la cartera es el sha256 del usuario pasado
    origin = hashlib.sha256(datajson['origin'].encode('utf-8')).hexdigest()
    key = datajson['key']
    #el id de la cartera es el sha256 del usuario pasado
    dest = hashlib.sha256(datajson['dest'].encode('utf-8')).hexdigest()
    quant = datajson['quant']
    date = int(time.time())

    #COMPROBAR QUE LA TRANSACCIÓN ES VALIDA
    if(user.check_user(origin, key) == False):
        return {"Code": 401, "description": "Authentication error"}    #UNAUTHORIZED
    if(user.check_quant(origin, quant) == False):
        return {"Code": 403, "description": "Insufficient balance"}    #FORBIDDEN

    #A partir de aquí la transacción está validada, actualicemos los usuarios
    user.act_quant(origin, dest, quant)

    trans = transaction(origin, dest, quant, date)    #Creamos el objeto transacción y lo guardamos en el pool
    globals.pool.append(trans)

    return {"Code": 202, "description": "Valid transaction"}         #ACCEPTED

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