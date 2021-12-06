
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 03:12:09 2021

@author: Marcos
"""


#Módulo 1: Crea una Blockchain

# Para instalar:
# Flask==0.12.2: pip install Flask==0.12.2
# Cliente HTTP Postman: https://www.getpostman.com/

#Importar las librerías
import datetime 
import hashlib #Librería de hashing
import json #Javascript object notation
from flask import Flask, jsonify #Flask = Constructor jsonify = Convertir a json.

#Parte 1 - Crear la cadena de Bloques
class Blockchain:
    
    def __init__(self):  #Creamos un constructor
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1, #Posición
                 'timestamp' : str(datetime.datetime.now()), #Fecha
                 'proof' : proof, #Prueba
                 'previous_hash': previous_hash} #Hash anterior
        self.chain.append(block) #Añadimos el bloque a la cadena.
        return block 
        
    def get_previous_block(self): #Creamos una función para obtener el bloque anterior.
        return self.chain[-1] #Devolvemos el último bloque de la cadena [-1].
    
    #Creando Proof of Work
    
    def proof_of_work(self, previous_proof): #Creamos una función para la prueba de trabajo.
        new_proof = 1 #Damos a como valor de origen 1
        check_proof = False #Valor de origen false.
        while check_proof is False: #Mientras que el valor sea false.
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() 
            #Necesitamos que la operación no sea simétrica
            #Porque facilitaría inmensamente el trabajo a los mineros y estos podrían minar toneladas y toneladas de bloques.
            if hash_operation[:4] == '0000':
                check_proof = True #Una vez que completemos los requisitos(operación), el valor pasará a ser True. Significará que hemos minado un nuevo bloque.
            else:
                new_proof += 1 #De lo contrario, crearemos un nuevo bloque.
        return new_proof 
    
    def hash(self, block): #Creamos una función para obtener el hash de un bloque.
        encoded_block = json.dumps(block, sort_keys = True).encode() #.dumps() realiza el volcado de nuestro diccionario a string.
        #Mediante sort.keys = True, aplicamos un orden alfabético a las claves. Mantenemos siempre un mismo orden.
        return hashlib.sha256(encoded_block).hexdigest() #.hexdigest() porque lo queremos en hexadecimal, esto hace que sea más entendible.
    
    def is_chain_valid(self, chain): #Función para saber si la cadena es válida.
        previous_block = chain[0] #Bloque Génesis
        block_index = 1 #Primer bloque de la cadena
        while block_index < len(chain): #Mantenemos la ejecución mientras block_index sea menor que la longitud de la cadena.
            current_block = chain[block_index] #Me proporciona el bloque en el que estamos actualmente.
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = current_block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block #El bloque anterior pasa a ser el bloque actual.
            block_index += 1 #Aumentamos en 1 el número de bloques.
        return True #Si todo sale como es debido, devolvemos True.
            
        
#Parte 2 - Minado de un Bloque de la Cadena

#Crear una aplicación web
app = Flask(__name__)


#Crear una Blockchain
blockchain = Blockchain()

#Minar un nuevo bloque
@app.route("/mine_block",methods=['GET'])
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
                







