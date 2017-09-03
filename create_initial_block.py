import datetime
from blockchain import Block

def create_initial_block():
    return Block(index=0, timestamp=datetime.datetime.now(), data='initial block', previous_hash='0')
