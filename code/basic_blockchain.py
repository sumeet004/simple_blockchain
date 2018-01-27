__author__ = '@drewrice2'

import os
import json
import hashlib
import datetime

from resources.block import Block
from resources.helper import proof_of_work


CHAIN_NAME = 'baby_chain.txt'


class Blockchain:

    def __init__(self):
        # path to chain
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.chainfile = os.path.join(dir_path, 'chain', CHAIN_NAME)

        self._create_chain_if_not_exists()

        # create genesis block if chainfile is empty
        if os.stat(self.chainfile).st_size == 0:
            self.create_genesis_block()

        self.data = []


    def _create_chain_if_not_exists(self):
        if not os.path.isfile(self.chainfile):
            f = open(self.chainfile,'w')
            f.close()


    def create_genesis_block(self):
        '''
        Creates the genesis block. Seperate routine due to the genesis block
            creation being a one-off event.
        '''
        b = Block(index=0,
            timestamp=str(datetime.datetime.now()),
            data='genesis block',
            previous_hash='0',
            nonce=1,
            num_zeroes=0)

        self.write_to_chain(b.get_block_data())


    def write_to_chain(self, block_dictionary):
        '''
        Writes a dictionary to json, appends the json to the blockchain
            text file.
        '''
        with open(self.chainfile, 'a') as f:
            f.write(json.dumps(block_dictionary) + '\n')
            f.close()


    def create_new_block(self):
        '''
        Creates a block using the data in `self.data`.
        '''
        with open(self.chainfile, 'r') as f:
            previous_block = f.readlines()[-1]
            previous_block = json.loads(previous_block)
            f.close()

        index = previous_block['index'] + 1
        previous_hash = previous_block['hash']
        timestamp = str(datetime.datetime.now())
        nonce, number_of_leading_zeroes = proof_of_work(previous_hash)

        self.block = Block(index=index,
            timestamp=timestamp,
            data=self.data,
            previous_hash=previous_hash,
            nonce=nonce,
            num_zeroes=number_of_leading_zeroes)

        self.write_to_chain(self.block.get_block_data())
        self.data = []


    def add_data_to_block(self, new_data):
        '''
        Appends data to the newest block.
        '''
        self.data.append(str(new_data))


    def validate_chain(self):
        '''
        Checks the chain for validity. Returns True on validation.
        '''
        with open(self.chainfile, 'r') as f:
            lines = f.readlines()
            f.close()

        for line in lines:
            block_to_validate = json.loads(line)
            number_of_zeroes = block_to_validate['num_zeroes']
            nonce = block_to_validate['nonce']
            previous_hash = block_to_validate['previous_hash']

            sha = hashlib.sha256()
            sha.update(
                str(previous_hash).encode('utf-8') +
                str(nonce).encode('utf-8')
                )
            challenge_hash = sha.hexdigest()

            if str(challenge_hash[:number_of_zeroes]) != "0" * number_of_zeroes:
                msg = 'Invalid chain.'
                raise ValueError(msg)

            return True




if __name__ == '__main__':
    b = Blockchain()
    for i in range(10):
        b.add_data_to_block('test_test_test')
        b.add_data_to_block('123345')
        b.add_data_to_block(i)
        b.create_new_block()
