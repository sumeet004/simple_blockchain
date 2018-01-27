## basic_blockchain.py

This code is an implementation of a lightweight, centralized blockchain. The
goal of this code to show an example of a blockchain to store any kind of data.

## transactional_node.py

A minimalist implementation of a Nakamoto transactional blockchain.

### Use

Change `PORT` and `peer_nodes` in `node.py` to launch more nodes. Communication
of transactions between nodes has not been implemented yet.

To retrieve the existing blockchain from a node:
```bash
curl -X GET -H "Content-Type: application/json" http://localhost:8060/blocks
```

To run the mining process and generate Blocks:
```bash
curl -X GET -H "Content-Type: application/json" http://localhost:8060/mine
```

To send a transaction to the node:

(Linux/UNIX)
```bash
curl -X POST -H "Content-Type: application/json" -d "{'to':'you',
  'from':'me','amount':10}" http://localhost:8060/transaction
```

(Windows)
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"to\":\"you\",
  \"from\":\"me\",\"amount\":10}" http://localhost:8060/transaction
```

---

### Future plans and other details

I plan to learn much more about the fundamentals of blockchain by way of
implementation. This repo began as a side project in a private repository. After
making some initial headway, I figured some people may be interested in Python
blockchains.

Constructive criticism and questions are welcomed! This implementation is far
from perfect; I will be refactoring and optimizing as time allows.

Aside from built-in Python packages, such as `json`, this implementation
requires:
- flask
- requests
- datetime

Install dependencies with:
```bash
pip install -r requirements.txt
```
