import json
from hashlib import sha256
from time import time


class Block:

    def __init__(self, uid, timestamp, transactions, previous_hash):
        self.uid = uid
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = None

    def compute_hash(self):
        data = json.dumps(self.__dict__)
        encoded = data.encode('UTF-8')
        return sha256(encoded).hexdigest()


class BlockChain:
    difficulty = 2

    def __init__(self):
        self.chain = [BlockChain.create_genesis_block()]

    @staticmethod
    def create_genesis_block():
        """TODO: explain genesis block"""
        return Block(0, time(), [], 'G E N E S I S')

    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block):
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not BlockChain.is_valid_hash(computed_hash):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    @staticmethod
    def is_valid_hash(block_hash):
        return block_hash.startswith('0' * BlockChain.difficulty)
