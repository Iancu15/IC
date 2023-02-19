'use strict';
const { Blockchain, Transaction, Block } = require('./blockchain');
const EC = require('elliptic').ec;
const ec = new EC('secp256k1');

// Your private key goes here
const myKey = ec.keyFromPrivate(
  '7c4c45907dec40c91bab3480c39032e90049f1a44f3e18c3e07c23e3273995cf'
);

const otherKey = ec.keyFromPrivate(
  '49aa4010ce070da34067ce6e6bb6683a7f87d982d0357774ada6c91a6bb55dcc'
);

// From that we can calculate your public key (which doubles as your wallet address)
const myWalletAddress = myKey.getPublic('hex');

const otherWalletAddress = otherKey.getPublic('hex');

// Create new instance of Blockchain classs
const savjeecoin = new Blockchain([myWalletAddress]);

//console.log(savjeecoin.chain[0].transactions)

savjeecoin.selectFirstValidator()

// Mint first block
savjeecoin.mintPendingTransactions(myWalletAddress);

// Create a transaction & sign it with your key
const tx1 = new Transaction(myWalletAddress, otherWalletAddress, 50);
tx1.signTransaction(myKey);
savjeecoin.addTransaction(tx1);

savjeecoin.selectValidator()

console.log(`selected validator tx1: ${savjeecoin.last_validator}`)

// Mint block
savjeecoin.mintPendingTransactions(myWalletAddress);

// Create second transaction
const tx2 = new Transaction(myWalletAddress, otherWalletAddress, 50);
tx2.signTransaction(myKey);
savjeecoin.addTransaction(tx2);

savjeecoin.selectValidator()

console.log(`selected validator tx2: ${savjeecoin.last_validator}`)

// Mine block
savjeecoin.mintPendingTransactions(myWalletAddress);

//console.log(savjeecoin)

console.log();
console.log(
  `Balance of xavier is ${savjeecoin.getBalanceOfAddress(myWalletAddress)}`
);

console.log();
console.log('Blockchain valid?', savjeecoin.isChainValid() ? 'Yes' : 'No');