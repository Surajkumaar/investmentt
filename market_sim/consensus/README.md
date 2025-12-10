# Market Simulation – Consensus Module

## Overview

This module implements distributed consensus protocols in Python, inspired by the Distributed Consensus book.
It focuses on Byzantine fault tolerance and synchronous consensus, including cryptographic signatures for message authentication.

## Features

- **Byzantine Broadcast**: Simplified Dolev–Strong protocol.
- **Dolev–Strong Broadcast**: Full protocol with signed messages and support for Byzantine nodes.
- **Synchronous Consensus**: Basic consensus using signed messages in a synchronous network.
- **Visualization**: Round-by-round message propagation for Dolev–Strong broadcast.
- **Unit Tests**: Verify correctness of all protocols.

## Folder Structure

```
consensus/
├── byzantine_broadcast.py
├── network.py
├── node.py
├── synchronous_consensus.py
├── utils/
│   └── crypto_utils.py
└── tests/
    ├── test_byzantine_broadcast.py
    ├── test_dolev_strong.py
    ├── test_synchronous_consensus.py
    └── visualize_dolev_strong.py
```

## How to Run

### Create and activate a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

### Run all tests:

```bash
pytest market_sim/consensus/tests/ -s
```

### Run the visualization:

```bash
python -m market_sim.consensus.tests.visualize_dolev_strong
```

All tests should pass, and the visualization will show messages per node per round.

## Results

- All nodes reach consensus correctly, even in the presence of Byzantine nodes.
- The simulation successfully demonstrates Dolev–Strong Byzantine Broadcast with cryptographic signatures.
