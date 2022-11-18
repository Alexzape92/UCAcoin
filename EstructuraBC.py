from hashlib import sha256 #Para cifrar las contraseñas de usuarios
import miner
from datetime import date  #Para el timestamp de los bloques
import os                  #Para acceder al json
import json                #.....

class globals:
    pool = list()   #lista de transacciones
    nextid = 0      #id del siguiente bloque a crear
    lasthash = 0    #hash del bloque anterior
    maxPoolSize = 100 #numero maximo de transacciones por bloque (he puesto 100 por poner)
    currentBlock = createBlock() #HAY QUE HACER QUE ESTA INICIALIZACION SE HAGA SOLO SI EL JSON ESTA VACIO

class block:
    def __init__(self, prev, nonce, time) -> None:
        self.prev = prev        #hash del bloque anterior
        self.hash               #hash del bloque
        self.roothash           #hash raiz (el de las transacciones)
        #self.dif = dif          #dificultad para el nonce del siguiente bloque
        self.nonce = nonce      #nonce del bloque
        self.time = time        #fecha y hora en la que se creó el bloque

class transaction:
    def __init__(self, usero, userd, cant) -> None:
        self.userd = userd      #id del usuario que recibe la transacción
        self.cant = cant        #cantidad de criptomonedas transferidas
        self.hash

class user:
    def __init__(self, id, key, quant) -> None:
        self.id = id            #id del usuario  
        self.key = key          #clave del usario (hash)
        self.quant = quant      #cantidad de criptomonedas del usuario
    
    def get_obj_us(id) -> user: #Este método accede a la base de datos de los usuarios y devueve el objeto user parseado
        return user()  
    
    def check_user(id, key) -> bool:
        us = user.get_obj_us(id)     
    
        return (us.key == key)
    
    def check_quant(id, quant) -> bool:
        us = user.get_obj_us(id)

        return (us.quant >= quant)



#devuelve el hash (usando sha256) del string
def hash(string):   
    return sha256(string.encode('utf-8').hexdigest())


#Hashea la transaccion a traves de el usuario destino y la cantidad
def hashTransaction(trans):     
    trans_str = str(trans.userd) + "-" + str(trans.quant)
    return hash(trans_str)


#Recibe una lista de transacciones y devuelve el hash raiz
def rootHash(transList):    
    root_str = ""
    for trans in transList:
            root_str += str(trans.hash)
    return hash(root_str)


#Hashea el bloque a traves de los hashes de sus transacciones, 
# el timestamp, y el hash del bloque anterior
def hashBlock(block):       
    block_str = str(block.rootHash) + "-" + str(block.time) + "-" + str(block.prev)    
    return hash(block_str)



#Este método registra un usuario en la base de datos con la id pasada
# #y la contraseña (sin cifrar), por lo que antes hay que hashearla
def register(id, passwd) -> None:   
    hashed_passwd = sha256(passwd.encode('utf-8').hexdigest())
    u = user(id, hashed_passwd, 0)  #este usuario hay que guardarlo en la base de datos
    return                          


#Solicitar una transacción
def transfer(origin, key, dest, quant):     
    if(user.check_user(origin, key) == False):
        raise Exception('CLAVE')
    if(user.check_quant(origin, quant) == False):
        raise Exception('CANTIDAD')
    #A partir de aquí la transacción está validada, podemos sacar los objetos
    ori = user.get_obj_us(origin)
    des = user.get_obj_us(dest)

    ori.quant -= quant
    des.quant += quant

    trans = transaction(dest, quant)    #Creamos el objeto transacción y lo guardamos en el pool
    globals.pool.append(trans)
    updateBlock(globals.currentBlock)


def updateJson(block, isNew):
    with open('blockchain.json', 'r+') as json_file:
        if (os.path.getsize("blockchain.json") == 0):   #Si el archivo esta vacio
            blockchain = {'block':[]}                   #creamos su estructura
        else: blockchain = json.load(json_file)
        json_file.seek(0)                               #Para poder reescribir el json, sin esto
        json_file.truncate(0)                           #solo podriamos añadir datos, no modificar
        if(isNew):
            #Añadimos el bloque
            blockchain['block'].append(block.__dict__) 
        else:
            #Actualizamos el ultimo bloque del json
            blockchain['block'][len(blockchain['block']-1)] = block.__dict__ 

        json.dump(blockchain, json_file, indent = 6, ensure_ascii=False)  
        json_file.close()


#Actualiza el hash del bloque actual y crea uno nuevo si es necesario
def updateBlock(block):  
    block.roothash = rootHash(globals.pool)
    block.hash = hashBlock(block)
    updateJson(block, False)
    if(len(globals.pool) == globals.maxPoolSize):
        createBlock()


#Crea un nuevo bloque y lo guarda en el fichero con la blockchain
def createBlock():      
    fechaHora = date.today()
    fechaHora_fixed = fechaHora.strftime("%d/%m/%Y %H:%M:%S")

    #FALTA PARAMETRO DE DIFICULTAD PARA SEARCHNONCE
    newBlock = block(globals.lasthash, miner.searchNonce(), fechaHora_fixed)
    newBlock.roothash = hash("null")                        #el bloque en este punto no tiene transacciones
    newBlock.hash = hashBlock(newBlock)

    updateJson(newBlock, True)

    #FALTA MANDAR A ACTUALIZAR LOS JSON DE TODA LA RED DE NODOS

    globals.pool = []
    globals.nextid += 1
    globals.lasthash = newBlock.hash

    return newBlock