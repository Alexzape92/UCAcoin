from __future__ import annotations
import requests
import time
import sqlite3

class globals:
    pool = list()   #lista de transacciones
    newxtid = 0     #id del siguiente bloque a crear
    lasthash = 0

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
        return 'id = {}, trans = {}, prev = {}, dif = {}, nonce = {}, tiempo = {}'.format(self.id, self.trans, self.prev, self.dif, self.nonce, self.time)

class transaction:
    def __init__(self, usero, userd, cant) -> None:
        self.usero = usero      #id del usuario que realiza la transacción
        self.userd = userd      #id del usuario que recibe la transacción
        self.cant = cant        #cantidad de criptomonedas transferidas

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

        cursor = cur.execute("SELECT * FROM Users WHERE id = '{}'".format(id))
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

        db.execute("UPDATE Users SET wallet = wallet - {} WHERE id = '{}'".format(q, id1))
        db.execute("UPDATE Users SET wallet = wallet + {} WHERE id = '{}'".format(q, id2))

        db.commit()
        db.close()


def register(id, passwd) -> None:   #Este método registra un usuario en la base de datos con la id pasada
    return                          #y la contraseña (sin cifrar), por lo que antes hay que hashearla

def transfer(origin, key, dest, quant):     #solicitar una transacción
    #COMPROBAR QUE LA TRANSACCIÓN ES VALIDA
    if(user.check_user(origin, key) == False):
        raise Exception('CLAVE')
    if(user.check_quant(origin, quant) == False):
        raise Exception('CANTIDAD')

    #A partir de aquí la transacción está validada, actualicemos los usuarios
    user.act_quant(origin, dest, quant)

    trans = transaction(origin, dest, quant)    #Creamos el objeto transacción y lo guardamos en el pool
    globals.pool.append(trans)


if __name__ == '__main__':
    transfer('Richarte2002', 'ElBarrio', 'AlexZape', 7.5)
