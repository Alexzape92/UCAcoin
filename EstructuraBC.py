from hashlib import sha256 #para cifrar las contraseñas de usuarios
import miner
from datetime import date

class globals:
    pool = list()   #lista de transacciones
    nextid = 0      #id del siguiente bloque a crear
    lasthash = 0    #hash del bloque anterior

class block:
    def __init__(self, id, n, trans, prev, dif, nonce, time) -> None:
        self.id = id            #id del bloque (profundidad del bloque)
        self.n = n              #número de transacciones en este bloque
        self.trans = trans      #lista de transacciones
        self.prev = prev        #hash del bloque anterior
        self.hash               #hash del bloque
        self.roothash           #hash raiz
        self.dif = dif          #dificultad para el nonce del siguiente bloque
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

def register(id, passwd) -> None:   #Este método registra un usuario en la base de datos con la id pasada
                                    #y la contraseña (sin cifrar), por lo que antes hay que hashearla
    hashed_passwd = sha256(passwd.encode('utf-8').hexdigest())
    u = user(id, hashed_passwd, 0)  #este usuario hay que guardarlo en la base de datos
    return                          

def transfer(origin, key, dest, quant):     #solicitar una transacción
    if(user.check_user(origin, key) == False):
        raise Exception('CLAVE')
    if(user.check_quant(origin, quant) == False):
        raise Exception('CANTIDAD')
    #A partir de aquí la transacción está validada, podemos sacar los objetos
    ori = user.get_obj_us(origin)
    des = user.get_obj_us(dest)

    ori.quant -= quant  #Transacción validadas, cambiamos las carteras de los usuarios
    des.quant += quant

    trans = transaction(dest, quant)    #Creamos el objeto transacción y lo guardamos en el pool
    globals.pool.append(trans)

def hashTransaction(trans):             #Hashea la transaccion a traves de el usuario destino y la cantidad
    trans_str str(trans.userd) + "-" + str(trans.quant)
    return sha256(trans_str.encode('utf-8').hexdigest())


def rootHash(transList):                     #Recibe una lista de transacciones y devuelve el hash raiz
    root_str = ""
    for t in transList:
            root_str += t.hash
    return sha256(root_str.encode('utf-8').hexdigest())


def hashBlock(block):                   #Hashea el bloque a traves de los hashes de sus transacciones, 
                                        #el timestamp, y el hash del bloque anterior
    block_str = str(block.rootHash) + "-" + str(block.time) + "-" str(block.prev)       


def createBlock():      #crea un nuevo bloque y lo guarda en el fichero con la blockchain
    with open('blockchain.json', 'r') as json_file:     #Cargamos el json con la blockchain
    if (os.path.getsize("blockchain.json") == 0): 
        blockchain = {block[]}  #Si el archivo esta vacio
    else: blockchain = json.load(json_file)
    json_file.close()

    fechaHora = date.today()
    fechaHora_fixed = fecha.strftime("%d/%m/%Y %H:%M:%S") #fecha y hora en formato dd/mm/YY H:M:S

    #faltan los parametros de dificultad y nonce
    newBlock = block(globals.nextid, globals.pool.len(), globals.pool, globals.lasthash, dificul, miner.searchNonce(), fecha_fixed)
    nesblock.roothash = rootHash(globals.pool)
    newblock.hash = hashBlock(newBlock)

    blockchain['block']append(block.__dict__)
    json_file =  open('blockchain.json', 'w', encoding="utf-8")
    json.dump(blockchain, json_file, indent = 6, ensure_ascii=False)  #Actualizamos el fichero json
    json_file.close()

    globals.pool = []   #vaciamos la lista de transacciones
    globals.nextid += 1
    globals.lasthash = newBlock.hash
