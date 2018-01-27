from pathlib import Path

CHAIN_NAME = 'baby_chain.txt'


chainfile = Path("./chain/" + CHAIN_NAME)
if chainfile.is_file():
    print('yup')
else:
    f = open(CHAIN_NAME,"w")
    f.write("test123")
    f.close()

# def write_blockchain():
#     f = open('file.txt','w')
#
# last_block = blockchain[len(blockchain) - 1]
# # perform proof of work function
# _previous_hash = last_block['hash']
# _nonce = _proof_of_work(_previous_hash)
# # reward miner
# this_nodes_transactions.append( {'from':'network', 'to':miner_address,
#     'amount':MINER_REWARD} )
# # generate new block's data, empty local transaction list
# _data = {'transactions':this_nodes_transactions}
# _index = int(last_block['index']) + 1
# _timestamp = str(datetime.datetime.now())
# mined_block = Block(index=_index, timestamp=_timestamp, data=_data,
#     previous_hash=_previous_hash, nonce=_nonce)
