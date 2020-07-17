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


def main():
    # create chain
    blockchain = BlockChain()
    print(f'blockchain = {blockchain.__dict__}')

    # create block
    uid = 1
    timestamp = time()
    transactions = ['{"name": "Transaction 1"}']
    previous_hash = blockchain.last_block().compute_hash()
    block = Block(uid, timestamp, transactions, previous_hash)
    print(f'block = {block.__dict__}')

    # create proof of work
    computed_hash = blockchain.proof_of_work(block)
    print(f'computed_hash = {computed_hash}')

    # append block
    blockchain.chain.append(block)
    print(f'blockchain = {blockchain.__dict__}')

    # verify blockchain
    last_hash = None
    for b in blockchain.chain:
        block_hash = b.compute_hash()
        if b.uid > 0:
            if not BlockChain.is_valid_hash(block_hash):
                raise Exception('Invalid hash')
            if last_hash != b.previous_hash:
                raise Exception('Invalid chain')
        elif b.uid == 0:
            pass  # genesis block; nothing to do
        else:
            raise Exception('Invalid uid')
        last_hash = block_hash

    print('blockchain is valid')


if __name__ == '__main__':
    main()
