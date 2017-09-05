from flask import Flask
from flask import request
import datetime
import requests
import hashlib
from requests.exceptions import ConnectionError
import json
from block import Block

# --------------------------------------------------------
#  node-specific data
this_nodes_transactions = []
PORT = 8060
peer_nodes = ["http://localhost:8090"]
miner_address = 'http://localhost:' + str(PORT)

# --------------------------------------------------------
# "private" functions
def _proof_of_work(previous_hash):
    nonce = None
    incrementor = 0
    NUM_ZEROES = 5
    while not nonce:
        sha = hashlib.sha256()
        sha.update(
            str(previous_hash).encode('utf-8') +
            str(incrementor).encode('utf-8')
            )
        challenge_hash = sha.hexdigest()
        if str(challenge_hash[:NUM_ZEROES]) == '0'*NUM_ZEROES:
            nonce = incrementor
        else:
            incrementor += 1
    return nonce

def _find_new_chains():
    """Find other chains.

    Except
        ConnectionError : on request failure
    """
    global peer_nodes
    # retrieve other nodes' blockchains
    other_chains = []
    for node_url in peer_nodes:
        try:
            # blockchain
            block = requests.get(node_url + "/blocks").content
            block = json.loads(block)
            other_chains.append(block)
        except ConnectionError:
            pass
    return other_chains

def _consensus():
    """Called on server start. Looks for alternative blockchains from
        members of `peer_nodes`.
    """
    other_chains = _find_new_chains()
    longest_chain = []
    if other_chains:
        for chain in other_chains:
            if len(longest_chain) < len(chain):
                longest_chain = chain
    # longest chain wins!
    return longest_chain

# --------------------------------------------------------
# REST API
node = Flask(__name__)

@node.route('/transaction', methods=['POST'])
def transaction():
    # TODO: broadcast to other nodes
    if request.method == 'POST':
        new_transaction = request.get_json()
        this_nodes_transactions.append(new_transaction)
        print("FROM: {}".format(new_transaction['from'].encode('ascii','replace')))
        print("TO: {}".format(new_transaction['to'].encode('ascii','replace')))
        print("AMOUNT: {}\n".format(new_transaction['amount']))
        return '~ transaction successful ~'

@node.route('/mine', methods=['GET'])
def mine():
    """Mining API code.

    Raises
        ValueError : when `mine()` is called on an empty `blockchain`
    """
    if not blockchain:
        msg = "Nothing to mine. Empty blockchain."
        raise ValueError(msg)

    global this_nodes_transactions
    # retrieve the last PoW
    last_block = blockchain[len(blockchain) - 1]
    # PoW
    _previous_hash = last_block['hash']
    _nonce = _proof_of_work(_previous_hash)
    # reward miner
    this_nodes_transactions.append( {'from':'network', 'to':miner_address,
        'amount':1} )
    # generate new block's data
    _data = {'transactions':this_nodes_transactions}
    _index = int(last_block['index']) + 1
    _timestamp = str(datetime.datetime.now())
    # empty transaction list
    this_nodes_transactions = []
    mined_block = Block(index=_index, timestamp=_timestamp, data=_data,
        previous_hash=_previous_hash, nonce=_nonce)

    mined_block_data = {'index':mined_block.index,
        'timestamp':mined_block.timestamp,
        'data':mined_block.data,
        'nonce':mined_block.nonce,
        'previous_hash':mined_block.previous_hash,
        'hash':mined_block.hash}

    blockchain.append(mined_block_data)

    # inform client of mining's completion
    mined = json.dumps(mined_block_data)
    print(mined+'\n')
    return mined

@node.route('/blocks', methods=['GET'])
def get_blocks():
    blocks = json.dumps(blockchain)
    print(blocks+'\n')
    return json.dumps(blocks)

# --------------------------------------------------------
# server initialization details
blockchain = _consensus()
# create first block if no other blockchain is available
if not blockchain:
    def create_initial_block():
        b = Block(index=0, timestamp=str(datetime.datetime.now()),
            data='initial block',
            previous_hash='0', nonce=1)

        return {'index':b.index,
            'timestamp':b.timestamp,
            'data':b.data,
            'nonce':b.nonce,
            'previous_hash':b.previous_hash,
            'hash':b.hash}

    blockchain = [create_initial_block()]
# run node
node.run(host='0.0.0.0', port=PORT, threaded=True, debug=False)