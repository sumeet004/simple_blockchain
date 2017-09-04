from flask import Flask
from flask import request
import datetime
import json
from block import Block, create_initial_block

node = Flask(__name__)

# node-specific data
this_nodes_transactions = []
peer_nodes = []

# node's copy of the blockchain
blockchain = []
blockchain.append(create_initial_block())

# mining boolean
MINING = True
miner_address = '123_your_address_here_456'

def next_block(last_block):
    _index = last_block.index + 1
    _timestamp = datetime.datetime.now()
    _data = "block #" + str(index)
    _hash = last_block.hash
    return Block(index=_index, timestamp=_timestamp, data=_data, previous_hash=_hash)

def proof_of_work(last_proof):
    # hyper basic PoW.
    incrementor = last_proof + 1
    while not ( (incrementor % 20000 == 0) and (incrementor % last_proof == 0) ):
        incrementor += 1
    return incrementor

@node.route('/transaction', methods=['POST'])
def transaction():
    if request.method == 'POST':
        global this_nodes_transactions
        new_transaction = request.get_json()
        this_nodes_transactions.append(new_transaction)
        print("FROM: {}".format(new_transaction['from'].encode('ascii','replace')))
        print("TO: {}".format(new_transaction['to'].encode('ascii','replace')))
        print("AMOUNT: {}\n".format(new_transaction['amount']))
        return '~ transaction successful ~'

@node.route('/mine', methods=['GET'])
def mine():
    global this_nodes_transactions
    global blockchain
    # retrieve the last PoW
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof_of_work']
    # PoW
    proof = proof_of_work(last_proof)
    # reward miner
    this_nodes_transactions.append( {"from":"network", "to":miner_address, "amount":1} )
    # generate new block's data
    _data = {"proof_of_work":proof, "transactions":this_nodes_transactions}
    _index = last_block.index + 1
    _timestamp = datetime.datetime.now()
    _hash = last_block.hash
    # empty transaction list
    this_nodes_transactions = []
    mined_block = Block(index=_index, timestamp=_timestamp, data=_data, previous_hash=_hash)
    blockchain.append(mined_block)
    # inform client of mining's completion
    return json.dumps(
        {"index":_index,
        "timestamp":str(_timestamp),
        "data":_data,
        "last_block_hash":_hash} )


@node.route('/blocks', methods=['GET'])
def get_blocks():
    global blockchain
    # communicate blockchain to other nodes
    chain_to_send = blockchain
    for block in chain_to_send:
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
    return json.dumps(chain_to_send)

def find_new_chains():
    # retrieve other nodes' blockchains
    other_chains = []
    for node_url in peer_nodes:
        # blockchain
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    # hyper basic consensus algorithm
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    # longest chain wins!
    blockchain = longest_chain

node.run(host='0.0.0.0', port=80, threaded=True, debug=False)
