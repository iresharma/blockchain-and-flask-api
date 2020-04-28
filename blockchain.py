from flask import Flask,jsonify
from datetime import datetime
import json
from hashlib import sha256
import random
import os


class Blockchain():

    def __init__(self):
        with open('chain.json', 'br') as ch:
            if len(ch.read()) == 0:
                self.chain = []
                self.createBlock()
            else:
                ch.seek(0)
                temp = ch.read()
                self.chain = json.loads(temp)

    def reload(self):
        with open('chain.json', 'br') as ch:
            temp = ch.read()
            self.chain = json.loads(temp)


    def createBlock(self):
        if len(self.chain) == 0:
            preHash = '0'
        else:
            preHash = self.chain[-1]['hash']
        block = {
            "index": len(self.chain) + 1,
            "preHash": preHash,
            "timeStamp": str(datetime.now()),
            "data": '',
            "nonce": 0,
            "mine": False,
            "hash": ''
        }
        print('hi')
        self.chain.append(block)
        with open('chain.json', 'w') as ch:
            json.dump(self.chain,ch,indent=4,ensure_ascii=True,sort_keys=True)
        return block

    def write(self, num, data):
        self.chain[num]['data'] = data
        for i in self.chain[num:]:
            i['mine'] = False

    def readBlock(self, num):
        return self.chain[num]

    def mine(self, num):
        check = False
        block = self.chain[num]
        while check == False:
            block['nonce'] = random.randint(0, 1000000000)
            hash = sha256(str(block).encode()).hexdigest()
            if hash[:4] == '0000':
                check = True
                block['hash'] = hash
                block['mine'] = True
        self.chain[num] = block
        with open('chain.json', 'w') as ch:
            json.dump(self.chain,ch,indent=4,ensure_ascii=True,sort_keys=True)






app = Flask(__name__)

blockchain = Blockchain()

@app.route('/')
def init():
    blockchain.reload()
    return jsonify(
        {
            "chain": blockchain.chain
        }
    )

@app.route('/makeBlock')
def makeBlock():
    blockchain.createBlock()
    blockchain.reload()
    return jsonify(
        {
            "chain": blockchain.chain
        }
    )

@app.route('/writeblock/<num>/<data>')
def writee(num, data):
    blockchain.write(int(num), data)
    blockchain.reload()
    return jsonify(
        {
            "chain": blockchain.chain
        }
    )

@app.route('/mine/<num>')
def mineA(num):
    if blockchain.chain[int(num)]['mine'] == False:
        blockchain.mine(int(num))
        blockchain.reload()
        return jsonify(
            {
                "chian": blockchain.chain
            }
        )
    else:
        return 'already mined'


if __name__ == "__main__":
    app.run()