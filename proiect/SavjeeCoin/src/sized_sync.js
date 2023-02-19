'use strict';
const { Blockchain, Transaction } = require('./blockchain')
const EC = require('elliptic').ec
const ec = new EC('secp256k1')

const private_keys = [
  '7c4c45907dec40c91bab3480c39032e90049f1a44f3e18c3e07c23e3273995cf',
  '49aa4010ce070da34067ce6e6bb6683a7f87d982d0357774ada6c91a6bb55dcc',
  'c9b6241199d3b74a92bb88d05cbe8eafa131d6fb789c9baf0b77e005ef18aa20',
  'dd48043e37a121810fa1c6ab65bbac43f9458d5dbfb00f166eebf4aa50c6e415'
]

const trusted_keys = []
const trusted_wallets = []
for (const private_key of private_keys) {
  trusted_keys.push(ec.keyFromPrivate(private_key))
  trusted_wallets.push(ec.keyFromPrivate(private_key).getPublic('hex'))
}

const adversary_key = ec.keyFromPrivate('d9a08a215a723f60ef766f7e87ca3d00cf78bc2218920dad61a2a8db143a60ab')
const adversary_wallet = adversary_key.getPublic('hex')

// create the two conflicting chains
const trusted_sized_blockchain = new Blockchain()
const untrusted_sized_blockchain = new Blockchain()

const trusted_hash_rates = [0.2, 0.2, 0.2, 0.3]
const adversary_hash_rate = [0.1]

// trusted chain mines blocks
trusted_sized_blockchain.minePendingTransactions(trusted_wallets[0])

// trusted chain makes some transaction and mines it
const tx1 = new Transaction(trusted_wallets[0], trusted_wallets[1], 100)
tx1.signTransaction(trusted_keys[0])
trusted_sized_blockchain.addTransaction(tx1)
trusted_sized_blockchain.minePendingTransactions(trusted_wallets[2])

// trusted chain makes another transaction and mines it
const tx2 = new Transaction(trusted_wallets[1], trusted_wallets[2], 50)
tx2.signTransaction(trusted_keys[1])
trusted_sized_blockchain.addTransaction(tx2)
trusted_sized_blockchain.minePendingTransactions(trusted_wallets[3])

// trusted chain makes another transaction and mines it
const tx3 = new Transaction(trusted_wallets[2], trusted_wallets[3], 50)
tx3.signTransaction(trusted_keys[2])
trusted_sized_blockchain.addTransaction(tx3)
trusted_sized_blockchain.minePendingTransactions(trusted_wallets[3])

// adversary copies trusted chain
untrusted_sized_blockchain.chain = [...trusted_sized_blockchain.chain]

// on a large amount of duration on average the adversary could mine 1 block
// 10% of the time
for (let i = 0; i < 100; i++) {
  const chosen_number = Math.random()
  if (chosen_number < 0.1) {
    untrusted_sized_blockchain.minePendingTransactions(adversary_wallet)
  } else {

    // if the adversary wasn't able to get ahead it copies the chain again
    untrusted_sized_blockchain.chain = [...trusted_sized_blockchain.chain]

    const tx4 = new Transaction(trusted_wallets[3], trusted_wallets[i % 3], 100)
    tx4.signTransaction(trusted_keys[3])
    trusted_sized_blockchain.addTransaction(tx4)
    trusted_sized_blockchain.minePendingTransactions(trusted_wallets[3])
  }
}

// though the chance of the adversary mining 6 blocks is 0.1^6 = 10^-6
// we can asume that in 10^6 iterations there's a high chance for it to mine
// 6 blocks

// sometime roughly 10^6 iterations later...

for (let i = 0; i < 6; i++) {
  untrusted_sized_blockchain.minePendingTransactions(adversary_wallet)
}

console.log();
console.log('Blockchain valid?', trusted_sized_blockchain.isChainValid() ? 'Yes' : 'No');

console.log();
console.log('Blockchain valid?', untrusted_sized_blockchain.isChainValid() ? 'Yes' : 'No');

// both blockchains are valid
// adversary broadcasts its blockchain to the trusted peers
// trusted peers see the adversary blockchain as being 6-7 blocks longer
// consider that chain as being the right chain
// the old chain isn't the notion of confirmation anymore, it isn't a certificate
// it's a subjective certificate
// the protocol is still secure if the 10^-6 chance is less than security parameter