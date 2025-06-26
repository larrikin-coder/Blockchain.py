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



class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    
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

    def new_transaction(self,sender,receiver,amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': receiver,
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
    
    