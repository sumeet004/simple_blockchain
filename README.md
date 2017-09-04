# simple_blockchain
A minimalist implementation of a transnational blockchain.

This repo was inspired by [Satoshi Nakamoto's blockchain whitepaper](https://bitcoin.org/bitcoin.pdf) and [Aunyks's tiny blockchain implementation in Python](https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173).

### Implementation

#### Nodes
Upon startup, nodes check for peers and their respective blockchains. If no peers are found, an initial block is created.

#### Consensus Algorithm
A blockchain is decided to be the master chain by evaluating lengths of other nodes' blockchains. The longest chain is decided to be the master blockchain. More complex consensus algorithms consensus algorithms can be implemented. For example, the longest chain with all transactions verified could be selected.

#### Mining
Mining from a node is a transactional relationship where the miner is rewarded for completing a very simple, yet verifiable mathematical task. Similar to the Proof of Work outlined in Nakamoto's whitepaper, this implementation requires a hash be created with a specified number of leading zero bits. This hash is a result of passing a string, made by concatenating a Block's previous hash and a nonce (the constant the miner is solving for), through the SHA256 hashing function. Once the nonce is solved for, the miner is rewarded and a new block is generated.   

### Use

To retrieve the existing blockchain from a node:
```bash
curl -X GET -H "Content-Type: application/json" http://localhost:80/blocks
```

To run the mining process and generate Blocks:
```bash
curl -X GET -H "Content-Type: application/json" http://localhost:80/mine
```
