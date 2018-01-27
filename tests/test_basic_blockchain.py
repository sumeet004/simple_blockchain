#!/usr/bin/env python


import unittest
import sys
import os

import path_magic

from basic_blockchain import Blockchain
from resources.helper import proof_of_work


class TestUM(unittest.TestCase):

    def setUp(self):
        self.b = Blockchain()


    def tearDown(self):
        pass


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


if __name__ == '__main__':
    unittest.main()
