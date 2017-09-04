from block import Block
from flask import Flask
import datetime
import json

parent = Flask(__name__)

def create_initial_block():
    return Block(index=0, timestamp=datetime.datetime.now(), data={'note':'initial block','proof_of_work':1}, previous_hash='0', nonce=1)

@parent.route('/blocks', methods=['GET'])
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

blockchain = [create_initial_block()]
parent.run(host='0.0.0.0', port=90, threaded=True, debug=False)
