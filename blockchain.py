#sample block

"""
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
"""

from time import time 
import hashlib
import json
from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify, request



class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1,proof=100)
    def new_block(self,proof,previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),  # Placeholder for timestamp
            'transactions': self.current_transactions,
            'proof': proof,  # Placeholder for proof
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self,sender,recipient,amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1;
    
    @staticmethod
    def hash(block):
        #creates sha256 hash
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof
    
    @staticmethod
    def valid_proof(last_proof,proof):
        #proves last 4 digits of hash are 0
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "00"
    
    
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', ''  )


blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    blockchain.new_transaction(
        sender = "0",
        recipient=node_identifier,
        amount=1
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof,previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/chain',methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ["sender","recipient","amount"]
    if not all(k in values for k in required):
        return 'Missing values',400
    index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
    response = {'message':f"transaction will be added to block {index}"}
    return jsonify(response), 201




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
    