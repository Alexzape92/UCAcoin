import requests

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
        return 'id = {}, trans = {}, prev = {}, dif = {}, nonce = {}'.format(self.id, self.trans, self.prev, self.dif, self.nonce)

class transaction:
    def __init__(self, usero, userd, cant) -> None:
        self.usero = usero      #id del usuario que realiza la transacción
        self.userd = userd      #id del usuario que recibe la transacción
        self.cant = cant        #cantidad de criptomonedas transferidas

class user:
    def __init__(self, id, key, wallet) -> None:
        self.id = id            #id del usuario  
        self.key = key          #clave del usario (hash)
        self.wallet = wallet    #cantidad de criptomonedas del usuario
    
    #def get_obj_us(id) -> user: #Este método accede a la base de datos de los usuarios y devueve el objeto user parseado
    #    return user()  
    
    def check_user(id, key) -> bool:
        us = user.get_obj_us(id)     
    
        return (us.key == key)
    
    def check_quant(id, quant) -> bool:
        us = user.get_obj_us(id)

        return (us.quant >= quant)

def register(id, passwd) -> None:   #Este método registra un usuario en la base de datos con la id pasada
    return                          #y la contraseña (sin cifrar), por lo que antes hay que hashearla

def transfer(origin, key, dest, quant):     #solicitar una transacción
    #if(user.check_user(origin, key) == False):
    #    raise Exception('CLAVE')
    #if(user.check_quant(origin, quant) == False):
    #    raise Exception('CANTIDAD')
    #A partir de aquí la transacción está validada, podemos sacar los objetos
    #ori = user.get_obj_us(origin)
    #des = user.get_obj_us(dest)

    #ori.quant -= quant  #Transacción validadas, cambiamos las carteras de los usuarios
    #des.quant += quant

    trans = transaction(origin, dest, quant)    #Creamos el objeto transacción y lo guardamos en el pool
    globals.pool.append(trans)

    nonce = requests.get(url='http://localhost:8000/getnonce/99999999').text

    print(nonce) 

if __name__ == '__main__':
    transfer(0, 'hola', 1, 10)
