
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
import json
from flask import Flask, jsonify

#Parte 1 - Crear la cadena de Bloques
class Blockchain:
    
    def __init__(self):  #Creamos un constructor
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
    
    #Creando Proof of Work
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() 
            #Necesitamos que la operación no sea simétrica
            #Porque facilitaría inmensamente el trabajo a los mineros y estos podrían minar toneladas y toneladas de bloques.
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode() #.dumps() realiza el volcado de nuestro diccionario a string.
        #Mediante sort.keys = True, aplicamos un orden alfabético a las claves. Mantenemos siempre un mismo orden.
        return hashlib.sha256(encoded_block).hexdigest()
        
#Parte 2 - Minado de un Bloque de la Cadena