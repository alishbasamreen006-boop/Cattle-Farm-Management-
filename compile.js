const solc = require('solc'); const fs = require('fs');
const src = fs.readFileSync('contracts/CattleRegistry.sol', 'utf8');
const input = { language: 'Solidity', sources: { 'CattleRegistry.sol': { content: src } },
  settings: { outputSelection: { '*': { '*': ['abi', 'evm.bytecode.object'] } } } };
const out = JSON.parse(solc.compile(JSON.stringify(input)));
if (out.errors) out.errors.forEach(e => console.log(e.formattedMessage));
const c = out.contracts['CattleRegistry.sol']['CattleRegistry'];
fs.writeFileSync('contracts/CattleRegistry.json', JSON.stringify({ abi: c.abi, bytecode: '0x' + c.evm.bytecode.object }, null, 2));
console.log('compiled OK');
