const { deriveHDKeyFromEthereumSignature } = require('@dydxprotocol/v4-client-js/build/src/lib/onboarding.js');
const { BECH32_PREFIX } = require('@dydxprotocol/v4-client-js/build/src');
const LocalWallet = require('@dydxprotocol/v4-client-js/build/src/clients/modules/local-wallet').default;
const { ethers } = require('ethers');
const fs = require('fs');

// ########################## YOU FILL THIS OUT #################
const mnemonic = '<FILL_THIS_OUT>'
// ##############################################################

const wallet = ethers.Wallet.fromPhrase(mnemonic);

const toSign = {
  "domain": {
    "name": "dYdX Chain",
    "chainId": 1
  },
  "primaryType": "dYdX",
  "types": {
    "EIP712Domain": [
      {
        "name": "name",
        "type": "string"
      },
      {
        "name": "chainId",
        "type": "uint256"
      }
    ],
    "dYdX": [
      {
        "name": "action",
        "type": "string"
      }
    ]
  },
  "message": {
    "action": "dYdX Chain Onboarding"
  }
};

(async () => {
  const signature = await wallet.signTypedData(toSign.domain, { dYdX: toSign.types.dYdX }, toSign.message);
  console.log('Signed Data:', signature);
  const k = deriveHDKeyFromEthereumSignature(signature);
  console.log('Mnemonic:', k.mnemonic);
  const lw = await LocalWallet.fromMnemonic(k.mnemonic, BECH32_PREFIX);
  console.log('Address:', lw.address)
})();
