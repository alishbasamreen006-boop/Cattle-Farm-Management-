# CattleChain - Blockchain-Based Cattle Farm Management (Demo)

## Run it (5 minutes)
```
python -m venv venv
venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```
Open the sidebar -> **Load dummy demo data**. Everything works with no wallet and no internet (local test chain).

## What the demo shows
1. Dashboard: animals, milk, expenses, profit, upcoming vaccinations
2. Animal Registry: add animal -> fingerprint saved on blockchain
3. Health Records (Vet role): vaccination/treatment signed on blockchain
4. Milk & Expenses: profit per animal (the BBA business angle)
5. Sell / Transfer: ownership change recorded on blockchain
6. Verify & QR: scan QR -> VERIFIED or TAMPERED. Use the "simulate tampering" box to show the panel.

## Files
- `app.py`        dashboard (Streamlit)
- `service.py`    saves to database + anchors hash on blockchain, and verifies
- `blockchain.py` talks to the smart contract (local chain or Sepolia)
- `db.py`         SQLite database
- `seed.py`       DUMMY data (replace with real interview data)
- `contracts/CattleRegistry.sol` the smart contract (Solidity)
- `contracts/CattleRegistry.json` compiled contract (already included)

## Stage 2: real public testnet (Sepolia)
1. Install MetaMask, create a NEW wallet used only for testing (never your real wallet).
2. Switch to Sepolia network and get free test ETH from a Sepolia faucet.
3. Copy `.env.example` values into your environment variables (RPC_URL from Alchemy/Infura free account, PRIVATE_KEY of the test wallet).
4. Run the app once: the terminal prints `CONTRACT DEPLOYED AT: 0x...`. Put it in CONTRACT_ADDRESS.
5. Every record now gets a real transaction hash. Paste it into https://sepolia.etherscan.io to show the panel.

## Honest limits (say these in your proposal)
- Only fingerprints go on-chain; details stay in the database.
- Blockchain proves a record was NOT changed AFTER saving. It cannot prove the first entry was truthful, so the vet's signature/role matters.
- Roles in this demo are a simple selector, not real login. Real login is future work.
- If you edit `contracts/CattleRegistry.sol`, recompile with `node compile.js` (needs `npm install solc@0.8.20`).
