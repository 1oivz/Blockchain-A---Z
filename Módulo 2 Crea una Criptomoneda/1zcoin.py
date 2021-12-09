# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 18:19:53 2021

@author: Marcos
"""

#Módulo 1: Crear una Criptomoneda

# Para instalar:
# Flask==0.12.2: pip install Flask==0.12.2
# Cliente HTTP Postman: https://www.getpostman.com/
# requests==2.26.0: pip install requests==2.26.0

#Importar las librerías
import datetime 
import hashlib 
import json 
from flask import Flask, jsonify, request #Request para hacer peticiones en una red descentralizada.
import requests #Checkear que todos los nodos de la red descentralizada tienen la misma blockchain, todos llegan a un consenso.
from uuid import uuid4
from urllib.parse import urlparse


# Parte 1 - Crear la cadena de Bloques

class Blockchain:
    
    def __init__(self):  #Constructor.
        self.chain = []
        self.transactions = [] #Creamos una lista vacía para las transacciones. La posición será antes del bloque génesis.
        self.create_block(proof = 1, previous_hash = '0')
        self.node_set = set() #Creamos un conjunto de nodos vacíos. Un conjunto significa que estos no tienen que seguir un orden.
        
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1, 
                 'timestamp' : str(datetime.datetime.now()), 
                 'proof' : proof, #Prueba
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = [] #Hay que vaciar de nuevo la lista puesto que las transacciones ya han sido añadidas en un bloque.
        #Una transacción solo puede aparecer en un bloque.
        self.chain.append(block) 
        return block 
        
    def get_previous_block(self):
        return self.chain[-1] 
    
    # Creando Proof of Work
    
    def proof_of_work(self, previous_proof): 
        new_proof = 1 
        check_proof = False 
        while check_proof is False: 
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() 
            if hash_operation[:4] == '0000':
                check_proof = True 
            else:
                new_proof += 1 
        return new_proof 
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        
        return hashlib.sha256(encoded_block).hexdigest() 
    
    def is_chain_valid(self, chain): 
        previous_block = chain[0] 
        block_index = 1 
        while block_index < len(chain): 
            current_block = chain[block_index] 
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = current_block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            block_index += 1 
        return True 
    
    def add_transaction(self, sender, receiver, amount): #Creamos la función donde añadiremos las transacciones hasta que se complete el bloque.
        self.transactions.append({'sender': sender,         
                                  'receiver': receiver, #Los argumentos de la función. Remitente, receptor y cantidad.
                                  'amount': amount})
        previous_block = self.previous_block() #Aplicamos self debido a que es un método de la propia clase aplicado al objeto que hemos recibido por parámetro.
        return previous_block['index'] + 1 #Devolvemos el bloque siguiente, que será el índice donde aparecerá esa transacción.
        #Tenemos que devolver el índice del nuevo bloque que se generará a continuación.
        
    
    def add_node(self, address): #Adress lo utilizamos para poder saber la dirección de ese nuevo nodo.
        parsed_url = urlparse(address)        
        self.nodes.add(parsed_url.netloc) #Me quedo solamente con el campo netloc, es decir, solo guardamos la dirección de cada uno de los nodos que se den de alta en nuestra criptomoneda.
        
# Parte 2 - Minado de un Bloque de la Cadena

# Crear una aplicación web
app = Flask(__name__)
#Si se obtiene un error 500, actualizar flask, reiniciar spyder y ejecutar la siguiente línea.
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Crear una Blockchain
blockchain = Blockchain()

# Minar un nuevo bloque
@app.route("/mine_block", methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block() #Obtenemos el bloque previo.
    previous_proof = previous_block['proof'] #Obtenemos la prueba de trabajo previa mediante la prueba del bloque anterior
    proof = blockchain.proof_of_work(previous_proof) #Obtenemos la prueba, mediante la prueba anterior de la función proof of work
    previous_hash = blockchain.hash(previous_block) #Obtenemos el hash anterior mediante el hash del bloque anterior
    block = blockchain.create_block(proof, previous_hash) #Obtenemos el bloque, mediante la prueba y hash previo de la función create_block
    #Para crear el bloque nuevo necesitamos la prueba de trabajo + el hash previo(bloque anterior).
    response = {'message': '¡Enhorabuena, has minado un nuevo bloque!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

#Obtener la cadena de bloques al completo.               
@app.route("/get_chain", methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#Comprobar si la Blockchain es válida.
@app.route("/is_valid", methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Correcto. La cadena de bloques es válida.'}
    else:
        response = {'message': 'Error. La cadena de bloques no es válida.'}
    return jsonify(response), 200


#Parte 3: Descentralizar la Blockchain.



# Ejecutar la app
app.run(host = '0.0.0.0', port = 5000)