'use strict';
const { Blockchain, Transaction, Block } = require('./blockchain');
const EC = require('elliptic').ec;
const ec = new EC('secp256k1');

const private_keys = [
  '7c4c45907dec40c91bab3480c39032e90049f1a44f3e18c3e07c23e3273995cf',
  '49aa4010ce070da34067ce6e6bb6683a7f87d982d0357774ada6c91a6bb55dcc',
  'c9b6241199d3b74a92bb88d05cbe8eafa131d6fb789c9baf0b77e005ef18aa20',
  'dd48043e37a121810fa1c6ab65bbac43f9458d5dbfb00f166eebf4aa50c6e415',
  'd9a08a215a723f60ef766f7e87ca3d00cf78bc2218920dad61a2a8db143a60ab' // <- adversary
]

const keys = []
const wallets = []
for (const private_key of private_keys) {
  keys.push(ec.keyFromPrivate(private_key))
  wallets.push(ec.keyFromPrivate(private_key).getPublic('hex'))
}

// Create new instance of Blockchain classs
const sync_blockchain = new Blockchain(wallets);

sync_blockchain.selectFirstValidator()

// Mint first block
for (const wallet of wallets) {
  sync_blockchain.mintPendingTransactions(wallet);
}

// Create a transaction & sign it with your key
const tx1 = new Transaction(wallets[0], wallets[1], 50);
tx1.signTransaction(keys[0]);
sync_blockchain.addTransaction(tx1);

sync_blockchain.selectValidator()

console.log(`selected validator tx1: ${sync_blockchain.last_validator}`)

// Mint block
for (const wallet of wallets) {
  sync_blockchain.mintPendingTransactions(wallet);
}

// Create second transaction
const tx2 = new Transaction(wallets[1], wallets[2], 50);
tx2.signTransaction(keys[1]);
sync_blockchain.addTransaction(tx2);

sync_blockchain.selectValidator()

console.log(`selected validator tx2: ${sync_blockchain.last_validator}`)

// Mine block
for (const wallet of wallets) {
  sync_blockchain.mintPendingTransactions(wallet);
}

for (const wallet of wallets) {
  console.log();
  console.log(
    `Balance of ${wallet} is ${sync_blockchain.getBalanceOfAddress(wallet)}`
  );
}

console.log();
console.log('Blockchain valid?', sync_blockchain.isChainValid() ? 'Yes' : 'No');

// adversary can create a fork and be the only one to mint blocks on that fork
// though the chance of the adversary minting 6 blocks is 0.2^6 = 6 * 10^-5
// in 1/6 * 10^5 = 0.17 * 10^5 = 1.7 * 10^4 iterations there's a high chance
// of double spending on multiple forks
// the problem is that since we have 5 wallets there's also high chance that
// during those 6 blocks it'll have to validate a block on the main chain
// and if it tries to create multiple forks each time it fails, it'll be highly
// suspicious on the chain and nobody will use that fork
// therefore it has to create a fork and try to build on it

sync_blockchain.createFork(wallets[4])

// let's though suppose that he'll be the only one to validate on the fork
// successive mints
let no_consecutive_mints = 0
let max_no_consecutive_mints = 0
for (let i = 0; i < 100; i++) {
  sync_blockchain.selectValidator()
  const tx4 = new Transaction(wallets[i % 4], wallets[(i + 1) % 4], 10)
  tx4.signTransaction(keys[i % 4])
  sync_blockchain.addTransaction(tx4)
  for (const wallet of wallets) {
    sync_blockchain.mintPendingTransactions(wallet);
  }

  // in parallel it tries mint on the fork
  const minted_on_fork = sync_blockchain.mintPendingTransactionsFork(wallets[4])
  if (minted_on_fork) {
    no_consecutive_mints++
  } else {
    if (no_consecutive_mints > max_no_consecutive_mints) {
      max_no_consecutive_mints = no_consecutive_mints
    }

    no_consecutive_mints = 0
  }
}

console.log(`Max number of consecutive mints: ${max_no_consecutive_mints}`)

// let's say that we had max_no_consecutive_mints = 10, then the additional
// fork would be behind 10 blocks behind
// but since we're in a partial synchronous setting, the adversary can delay
// the delivery of the following 15 blocks let's say on the main fork
// so that it can mint uninterrupted on the additional fork and gain 5 blocks
// ahead of the main fork
// that is best case, actually it'll have to mint way more blocks than that
// let's say 30 for good measure

// asynchronous interval
sync_blockchain.last_validator = null
for (let i = 0; i < 30; i++) {
    sync_blockchain.mintPendingTransactionsFork(wallets[4])
}

console.log(`Size main fork: ${sync_blockchain.chain.length}`)
console.log(`Size additional fork: ${sync_blockchain.fork.length}`)

// though even if it has the bigger fork, it'll have to convince somehow
// the other minters to go his fork
// if it somehow convinces them then the main fork's won't be a notion of
// confirmation anymore and therefore the blockchain won't produce certificates
// the paper only confirmed certificates after recalibration for PoS protocols in
// synchronous setting
// when we're talking about partial synchronous setting it matters greatly upon the
// implementation, not on simply being a PoS protocol of 'standard functionality'
// therefore the protocol would need something in place that prohibits leaving the
// main fork, in that case it would produce certificates