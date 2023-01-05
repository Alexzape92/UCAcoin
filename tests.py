import requests
import json

def testRegister():
    print("TESTS REGISTRAR CARTERA-----------------------------------------------------------\n")
    #Aquí registramos una nueva cartera (debería tener éxito)
    data = {"username": "Pepito"}
    jsonres = requests.get(url='http://localhost:8081/Register', json=data).text

    if(json.loads(jsonres)['Code'] == 201):
        print("Registrar usuario válido: PASS")
    else:
        print("Registrar usuario válido: FAIL")

    #Aquí registramos de nuevo la misma cartera (no debería dejar registrar dos carteras con el mismo nombre)
    jsonres = requests.get(url='http://localhost:8081/Register', json=data).text

    if(json.loads(jsonres)['Code'] == 201):
        print("Registrar usuario repetido: FAIL")
    else:
        print("Registrar usuario repetido: PASS")

    #Aquí registramos una cartera cuyo nombre de usuario está vacío (tampoco debería dejar)
    data2 = {"username": ""}
    jsonres = requests.get(url='http://localhost:8081/Register', json=data2).text

    if(json.loads(jsonres)['Code'] == 201):
        print("Registrar usuario vacío: FAIL")
    else:
        print("Registrar usuario vacío: PASS")
    
def testTransfer():
    print("\nTESTS SOLICITAR TRANSFERENCIA------------------------------------------\n")
    #Comprobar transacciones válidas
    data = {"origin": "root", "key": "e39a1ca80a756fe4f460ca69b2639eb8661cfdf443ea51f861d14fbc2d65f8fc", "dest": "Pepito", "quant": 5}

    jsonres = requests.post(url='http://localhost:8081/Transfer', json=data).text

    if json.loads(jsonres)['Code'] == 202:
        print("TRANSACCIÓN VÁLIDA: PASS")
    else:
        print("TRANSACCIÓN VÁLIDA: FAIL")
    
    #Comprobar transacciones en la que la clave privada del que la realiza no es la correcta
    data = {"origin": "root", "key": "hola", "dest": "Pepito", "quant": 5}

    jsonres = requests.post(url='http://localhost:8081/Transfer', json=data).text

    if json.loads(jsonres)['Code'] == 202:
        print("CLAVE INCORRECTA: FAIL")
    else:
        print("CLAVE INCORRECTA: PASS")

    #Comprobar transacciones en la que la cantidad a transferir es <= 0
    data = {"origin": "root", "key": "e39a1ca80a756fe4f460ca69b2639eb8661cfdf443ea51f861d14fbc2d65f8fc", "dest": "Pepito", "quant": -20}

    jsonres = requests.post(url='http://localhost:8081/Transfer', json=data).text

    if json.loads(jsonres)['Code'] == 202:
        print("CANTIDAD INCORRECTA: FAIL")
    else:
        print("CANTIDAD INCORRECTA: PASS")

    #Comprobar transacciones en la que la cantidad a transferir es mayor que el saldo del que la envúía
    data = {"origin": "root", "key": "e39a1ca80a756fe4f460ca69b2639eb8661cfdf443ea51f861d14fbc2d65f8fc", "dest": "Pepito", "quant": 2000000}

    jsonres = requests.post(url='http://localhost:8081/Transfer', json=data).text

    if json.loads(jsonres)['Code'] == 202:
        print("CANTIDAD MAYOR QUE EL SALDO: FAIL")
    else:
        print("CANTIDAD MAYOR QUE EL SALDO: PASS")

    #Comprobar transacciones en la que el usuario destino no existe
    data = {"origin": "root", "key": "e39a1ca80a756fe4f460ca69b2639eb8661cfdf443ea51f861d14fbc2d65f8fc", "dest": "holaquetal", "quant": 2000000}

    jsonres = requests.post(url='http://localhost:8081/Transfer', json=data).text

    if json.loads(jsonres)['Code'] == 202:
        print("USUARIO DESTINO INCORRECTO: FAIL")
    else:
        print("USUARIO DESTINO INCORRECTO: PASS")

def testBalance():
    print("\nTESTS SOLICITAR SALDO--------------------------------------------------\n")
    #Comprobar peticiones válidas
    data = {"username": "root", "private_key": "e39a1ca80a756fe4f460ca69b2639eb8661cfdf443ea51f861d14fbc2d65f8fc"}

    jsonres = requests.get(url='http://localhost:8081/Balance', json=data).text

    if json.loads(jsonres)['Code'] == 200:
        print("PETICIÓN VÁLIDA: PASS")
    else:
        print("PETICIÓN VÁLIDA: FAIL")
    
    #Comprobar peticiones en la que la clave privada del que la solicita no es la correcta
    data = {"username": "root", "private_key": "hola"}

    jsonres = requests.get(url='http://localhost:8081/Balance', json=data).text

    if json.loads(jsonres)['Code'] == 200:
        print("CLAVE INCORRECTA: FAIL")
    else:
        print("CLAVE INCORRECTA: PASS")

testRegister()
testTransfer()
testBalance()