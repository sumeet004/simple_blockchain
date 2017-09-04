# simple_blockchain
A minimalist implementation of a transnational blockchain.

This repo was inspired by [Satoshi Nakamoto's blockchain whitepaper](https://bitcoin.org/bitcoin.pdf) and [Aunyks's tiny blockchain implementation in Python](https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173).

---

### Implementation

#### Blocks!
A block is an object that contains, in this implementation, a series of transactional data. All previous transactions are available in a public ledger called the blockchain. A blockchain is a sequence of blocks available for inspection. Thus the integrity of the whole system can be determined to be valid by verifying all blocks in reverse chronological order all the way back to the first created block. The validity of the blocks is determined by using a Proof of Work algorithm. More on that later.

#### Nodes
Upon startup, nodes check for peers and their respective blockchains. If no peers are found, an initial block is created.

#### Consensus Algorithm
A blockchain is decided to be the master chain by evaluating lengths of other nodes' blockchains. The longest chain is decided to be the master blockchain. More complex consensus algorithms consensus algorithms can be implemented. For example, the longest chain with all transactions verified could be selected.

#### Mining
Mining from a node is a transactional relationship where the miner is rewarded for completing a very simple, yet verifiable mathematical task. Similar to the Proof of Work outlined in Nakamoto's whitepaper, this implementation requires a hash be created with a specified number of leading zero bits. This hash is a result of passing a string, made by concatenating a Block's previous hash and a nonce (the constant the miner is solving for), through the SHA256 hashing function. Once the nonce is solved for, the miner is rewarded and a new block is generated.   

---

### Use

Change `PORT` and `peer_nodes` in `node.py` to launch more nodes. Communication of transactions between nodes has not been implemented yet.

To retrieve the existing blockchain from a node:
```bash
curl -X GET -H "Content-Type: application/json" http://localhost:80/blocks
```

To run the mining process and generate Blocks:
```bash
curl -X GET -H "Content-Type: application/json" http://localhost:80/mine
```

To send a transaction to the node:
```bash
curl -X POST -H "Content-Type: application/json" -d "{'to':'you',
  'from':'me','amount':10}" http://localhost:90/transaction
```

---

### Future plans and other details

I plan to learn much more about the fundamentals of blockchain by way of implementation. This repo began as a side project in a private repository. After making some initial headway, I figured some people may be interested in Python blockchains.

Constructive criticism and questions are welcomed! This implementation is far from perfect; I will be refactoring and optimizing as time allows.

Aside from built-in Python packages, such as `json`, this implementation requires:
- flask
- requests
- datetime

Install dependencies with:
```bash
pip install -r requirements.txt
```
