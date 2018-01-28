#!/usr/bin/env python
"""
An implementation of a lightweight, centralized blockchain to store any kind of
    data.
"""
__author__ = '@drewrice2'

import os
import json
import hashlib
import datetime

from resources.block import Block
from resources.helper import proof_of_work


# TODO: s3 integration for blockchain.txt
# TODO: implement multi-file blockchain support


CHAIN_NAME = 'baby_chain.txt'


class Blockchain:

    def __init__(self):
        # path to chain
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.chainfile = os.path.join(dir_path, 'chain', CHAIN_NAME)

        self._create_chain_if_not_exists()

        # create genesis block if chainfile is empty
        if os.stat(self.chainfile).st_size == 0:
            self._create_genesis_block()

        self.data = []


    def _create_chain_if_not_exists(self):
        if not os.path.isfile(self.chainfile):
            f = open(self.chainfile,'w')
            f.close()


    def _create_genesis_block(self):
        '''
        Creates the genesis block. Seperate routine due to the genesis block
            creation being a one-off event.
        '''
        b = Block(index=0,
            timestamp=str(datetime.datetime.now()),
            data='genesis block',
            previous_hash='0',
            nonce=1,
            num_zeros=0)

        self._write_to_chain(b.get_block_data())


    def _write_to_chain(self, block_dictionary):
        '''
        Writes a dictionary to json, appends the json to the blockchain text
            file.
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
        nonce, number_of_leading_zeros = proof_of_work(previous_hash)

        self.block = Block(index=index,
            timestamp=timestamp,
            data=self.data,
            previous_hash=previous_hash,
            nonce=nonce,
            num_zeros=number_of_leading_zeros)

        self._write_to_chain(self.block.get_block_data())
        self.data = []


    def add_data_to_block(self, new_data):
        '''
        Appends data to the newest block.
        '''
        self.data.append(str(new_data))


    def _return_hash(self, previous_hash, nonce):
        sha = hashlib.sha256()
        sha.update(
            str(previous_hash).encode('utf-8') +
            str(nonce).encode('utf-8')
            )
        return sha.hexdigest()


    def _validate_hash(self, _hash, num_zeros):
        if str(_hash[:num_zeros]) != "0" * num_zeros:
            msg = 'Invalid chain.'
            raise ValueError(msg)
        else:
            return True


    def validate_chain(self, chain=''):
        '''
        Checks the chain for validity. Returns True on validation.
        '''
        if not chain:
            chain = self.chainfile
        with open(chain, 'r') as f:
            lines = f.readlines()
            f.close()

        for line in lines:
            block_to_validate = json.loads(line)
            number_of_zeros = block_to_validate['num_zeros']
            nonce = block_to_validate['nonce']
            previous_hash = block_to_validate['previous_hash']

            _hash = self._return_hash(previous_hash, nonce)
            self._validate_hash(_hash, number_of_zeros)

        return True


if __name__ == '__main__':
    b = Blockchain()
    # b.add_data_to_block('this is some data!')
    # b.create_new_block()
    b.validate_chain()
