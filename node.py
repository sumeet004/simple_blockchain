from flask import Flask
from flask import request
import datetime
import requests
import hashlib
from requests.exceptions import ConnectionError
import json
from block import Block

node = Flask(__name__)

# node-specific data
this_nodes_transactions = []
peer_nodes = ["http://localhost:90"]

# mining boolean
miner_address = 'http://localhost:80'

def startup():
    global blockchain
    blockchain = consensus()

def proof_of_work(block):
    last_proof = block.data['proof_of_work']
    block_hash = block.hash
    # check hash validity
    sha = hashlib.sha256()
    sha.update(
        str(block.index).encode('utf-8') +
        str(block.timestamp).encode('utf-8') +
        str(block.data).encode('utf-8') +
        str(block.previous_hash).encode('utf-8') +
        str(block.nonce).encode('utf-8')
        )
    if block_hash == sha.hexdigest():
        return b



    # hyper basic PoW.
    incrementor = last_proof + 1
    while not ( (incrementor % 20000 == 0) and (incrementor % last_proof == 0) ):
        incrementor += 1
    return incrementor

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
    """
    Mining API code.

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
    proof = proof_of_work(last_block)

    new_hash = x

    # reward miner
    this_nodes_transactions.append( {"from":"network", "to":miner_address,
        "amount":1} )
    # generate new block's data
    _data = {"proof_of_work":proof, "transactions":this_nodes_transactions}
    _index = last_block.index + 1
    _timestamp = datetime.datetime.now()
    _hash = last_block.hash
    _nonce = last_block.nonce
    # empty transaction list
    this_nodes_transactions = []
    mined_block = Block(index=_index, timestamp=_timestamp, data=_data,
        previous_hash=_hash, nonce=_nonce)
    blockchain.append(mined_block)
    # inform client of mining's completion
    return json.dumps(
        {"index":_index,
        "timestamp":str(_timestamp),
        "data":_data,
        "last_block_hash":_hash} )


@node.route('/blocks', methods=['GET'])
def get_blocks():
    # retrieve this node's copy of the blockchain to return
    this_nodes_blockchain = blockchain
    # create empty JSON string to return to client
    chain_to_send = ""
    for i in range( len(this_nodes_blockchain) ):
        block = this_nodes_blockchain[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = {
          "index": block_index,
          "timestamp": block_timestamp,
          "data": block_data,
          "hash": block_hash
        }
        # add block to response
        json_block = json.dumps(block)
        if chain_to_send == "":
            chain_to_send = json_block
        else:
            chain_to_send += json_block
    return chain_to_send

def find_new_chains():
    """
    Find other chains.

    Except
        ConnectionError : on request failure
    """
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

def consensus():
    # hyper basic consensus algorithm
    other_chains = find_new_chains()
    longest_chain = []
    if other_chains:
        for chain in other_chains:
            if len(longest_chain) < len(chain):
                longest_chain = chain
    # longest chain wins!
    return longest_chain

startup()
print(blockchain)
node.run(host='0.0.0.0', port=80, threaded=True, debug=False)
