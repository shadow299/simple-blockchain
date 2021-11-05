# module 1 : create a blockchain

#imports
import datetime
import hashlib
import json
from flask import Flask, jsonify

#part 1 : building the blockchain

class Blockchain:
    def __init__(self):
        self.chain = []
        # genesis block
        self.create_block(proof = 1, privious_hash = '0')

    def create_block(self, proof, privious_hash):
        block = {
            'index': len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'privious_hash' : privious_hash
        }
        self.chain.append(block)
        return block

    def get_privious_block(self):
        return self.chain[-1]

    def proof_of_work(self, privious_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_opration = hashlib.sha256(str(new_proof**2 - privious_proof**2).encode()).hexdigest()
            if hash_opration[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        print(hash_opration)
        return new_proof
        

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        privious_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['privious_hash'] != self.hash(privious_block):
                return False
            privious_proof = privious_block['proof']
            proof = block['proof']
            hash_opration = hashlib.sha256(str(proof**2 - privious_proof**2).encode()).hexdigest()
            if hash_opration[:4] != '0000':
                return False
            privious_block = block
            block_index += 1
        return True




# part 2 : mining the blockchain

# creating webapp using Flask

app = Flask(__name__)
bkchain = Blockchain()

# mining the blockchain
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    privious_block = bkchain.get_privious_block()
    privious_proof = privious_block['proof']
    proof = bkchain.proof_of_work(privious_proof)
    privious_hash = bkchain.hash(privious_block)
    block = bkchain.create_block(proof, privious_hash)
    response = {'message': 'congratulation you just mined a block.',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'privious_hash' : block['privious_hash']
                }
    return jsonify(response), 200

# getting the full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': bkchain.chain,
                'length': len(bkchain.chain)}
    return jsonify(response), 200


@app.route('is_valid', method=['GET'])
def is_valid():
    is_valid = bkchain.is_chain_valid(bkchain.chain)
    if is_valid:
        rp = {'message' : 'all good chain is valid'}
    else:
        rp = {'message' : 'we have a problem. blockchain is not valid.'}
    return jsonify(rp), 200

#Running the app
app.run(host = '0.0.0.0', port = 5000)