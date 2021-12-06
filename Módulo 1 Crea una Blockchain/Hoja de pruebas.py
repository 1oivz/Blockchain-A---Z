# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 18:03:57 2021

@author: Marcos
"""

#Módulo 1: Crear una blockchain.

import datetime #Para trabajar con fechas, puesto que cada hash va a tener su datetime.
import hashlib #Librería de hashing (hash).
import json #Javascript object notation
from flask import Flask, jsonify #De flask, importamos Flask = Constructor y jsonify para pasar a json.

#Parte 1: Crear la Blockchain.

class Blockchain: #Inicializamos la clase Blockchain.
    
    def __init__(self): #Inicializamos el constructor, self para especificar que estamos pasando el valor a los atributos de la instancia y no a la variable o argumento local con el mismo nombre.
        self.chain = [] #Creamos una lista vacía para la cadena.
        self.creat_block(proof = 1, previous_block = '0') #Ponemos el '0' así porque queremos mantener en formato string.
        
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain)+1,
            'timestamp': datetime.datetime.now(),
            'proof' : proof,
            'previous_hash' : previous_hash}
        self.chain.append(block)
        return block
    
    
    def get_previous_block(self):
        return self.chain[-1]
    
    
    #Crear Proof of Work
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() 
            #Utilizamos el método .encode(para codificar el string y así este en el formato adecuado que espera la librería hashlib (Añadirlo correctamente))
            #El sha256 nos devolverá un valor hexadecimal, por eso le aplicamos el .hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof +=1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain(block_index)
                