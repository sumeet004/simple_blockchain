## basic_blockchain.py

This code is an implementation of a lightweight blockchain. In this current
state, the blockchain should be able to store any kind of text data.

On instantiation, the Blockchain object will:
1. Create an empty chainfile with a genesis block if it cannot find one in
`code/chain/`.
2. Run `self.validate_chain()` and confirm the existing chain is valid

This code assumes:
- The blockchain exists in a text file ( in `code/chain/` ).
- Only one block may have an index of "0". This is called the genesis block.
- Hashes are stored sequentially, in json form.

#### TODOs
There are a few things that could greatly improve usage.

I would like to implement a better data storage format than appending data
in `.json` to a text file.

Parameterized storage would be great for extensibility. In other words, support
for multi-file blockchains. Additionally, chainfiles stored remotely
( in Amazon S3, for example ) would be a great addition.
