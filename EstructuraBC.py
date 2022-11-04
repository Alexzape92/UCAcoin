from hashlib import sha256 #Para hashear las contraseñas

class globals:
    pool = list()

class block:
    def __init__(self, id, n, trans, prev, dif, nonce, time) -> None:
        self.id = id            #id del bloque (profundidad del bloque)
        self.n = n              #número de transacciones en este bloque
        self.trans = trans      #lista de transacciones
        self.prev = prev        #hash del bloque anterior
        self.dif = dif          #dificultad para el nonce del siguiente bloque
        self.nonce = nonce      #nonce del bloque
        self.time = time        #fecha y hora en la que se creó el bloque

class transaction:
    def __init__(self, usero, userd, cant) -> None:
        self.usero = usero      #id del usuario que realiza la transacción
        self.userd = userd      #id del usuario que recibe la transacción
        self.cant = cant        #cantidad de criptomonedas transferidas

class user:
    def __init__(self, id, key, quant) -> None:
        self.id = id            #id del usuario  
        self.key = key          #clave del usario (hash)
        self.quant = quant    #cantidad de criptomonedas del usuario
    
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
    hashedPasswd = sha256(passwd.encode("utf-8")).hexdigest()     
    us = user(id, hashedPasswd, 0)  #Este objeto hay que guardarlo en la base de datos ()
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

    trans = transaction(origin, dest, quant)    #Creamos el objeto transacción y lo guardamos en el pool
    globals.pool.append(trans)



