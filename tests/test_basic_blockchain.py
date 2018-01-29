#!/usr/bin/env python
"""
Basic tests for some of the blockchain code.
"""
__author__ = '@drewrice2'

import unittest
import json
import sys
import os

import path_magic
from basic_blockchain import Blockchain
from resources.helper import proof_of_work


class TestUM(unittest.TestCase):

    def setUp(self):
        self.b = Blockchain()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))


    def tearDown(self):
        pass


    def test_validate_hash(self):
        h = '000006'
        nonce = '725237'
        num_zeros = 5

        passing_zeros = num_zeros
        failing_zeros = num_zeros + 1
        self.assertTrue(self.b._validate_hash(h, passing_zeros))
        self.assertRaises(ValueError, self.b._validate_hash, h, failing_zeros)


    def test_return_hash(self):
        h = 'a29ae45f7a73f21ae926031f0de7d78ea19d299dadef7fb5c0e5d178a82fc11c'
        nonce = '725237'
        num_zeros = 5
        passing_zeros = "0" * num_zeros
        failing_zeros = "0" * (num_zeros + 1)
        self.assertEqual(
            self.b._return_hash(previous_hash=h, nonce=nonce)[:num_zeros],
            passing_zeros)

        self.assertNotEqual(
            self.b._return_hash(previous_hash=h, nonce=nonce)[:num_zeros],
            failing_zeros)


    def test_proof_of_work(self):
        h = 'a29ae45f7a73f21ae926031f0de7d78ea19d299dadef7fb5c0e5d178a82fc11c'
        nonce = 725237
        num_zeros = 5
        _nonce, _num_zeros = proof_of_work(h, num_zeros)
        self.assertEqual(_nonce, nonce)
        self.assertNotEqual(_nonce+1, nonce)


    def test_write_to_chain(self):
        chainfile = 'chain_blank.txt'
        self.b.chainfile = os.path.join(self.dir_path, 'test_data', chainfile)

        test_dict = {"test_data": "check123"}

        def test_dict_exists_in_chain(test_dict):
            with open(self.b.chainfile, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line == json.dumps(test_dict)+'\n':
                        return True
                return False

        # validate test dict isn't in blockchain
        self.assertFalse(test_dict_exists_in_chain(test_dict))

        # write to chain
        self.b._write_to_chain(test_dict)
        self.assertTrue(test_dict_exists_in_chain(test_dict))

        def delete_last_line():
            # read into memory
            with open(self.b.chainfile) as f:
                lines = f.readlines()
            # remove last line
            with open(self.b.chainfile,'w') as w:
                w.writelines([item for item in lines[:-1]])

        delete_last_line()
        # validate test dict isn't in blockchain
        self.assertFalse(test_dict_exists_in_chain(test_dict))


    def test_multiple_blocks_at_index_0(self):
        # validate that a chainfile can only have one entry with an index of 1
        chainfile = 'chain_multiple_index_zero.txt'
        self.b.chainfile = os.path.join(self.dir_path, 'test_data', chainfile)

        self.assertRaises(ValueError, self.b.validate_chain)


    def test_correct_previous_hash(self):
        # valid chain test
        chainfile = 'chain_valid.txt'
        self.b.chainfile = os.path.join(self.dir_path, 'test_data', chainfile)
        self.assertTrue(self.b.validate_chain())

        # test `hash` and `previous_hash` validation
        chainfile = 'chain_incorrect_previous_hash.txt'
        self.b.chainfile = os.path.join(self.dir_path, 'test_data', chainfile)
        self.assertRaises(ValueError, self.b.validate_chain)


if __name__ == '__main__':
    unittest.main()
