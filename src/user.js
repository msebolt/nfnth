
if (typeof window.ethereum !== 'undefined') {console.log('MetaMask is installed!'); }
async function signer() { const accounts = await ethereum.request({ method: 'eth_requestAccounts' }); const account = accounts[0]; alert(account); }

//	const transactionParameters = {
  //nonce: '0x00', // ignored by MetaMask
  //gasPrice: '0x09184e72a000', // customizable by user during MetaMask confirmation.
  //gas: '0x2710', // customizable by user during MetaMask confirmation.
  //to: '0x0000000000000000000000000000000000000000', // Required except during contract publications.
  //from: ethereum.selectedAddress, // must match user's active address.
  //value: '0x00', // Only required to send ether to the recipient from the initiating external account.
  //data:
  //  '0x7f7465737432000000000000000000000000000000000000000000000000000000600057', // Optional, but used for defining smart contract creation and interaction.
 // chainId: '0x3', // Used to prevent transaction reuse across blockchains. Auto-filled by MetaMask.
//};

//const txHash = await ethereum.request({
//  method: 'eth_sendTransaction',
//  params: [transactionParameters],
//});

signTypedDataV4Button.addEventListener('click', function (event) {
  event.preventDefault();

  const msgParams = JSON.stringify({
    domain: { chainId: 1, // Defining the chain aka Rinkeby testnet or Ethereum Main Net
    name: 'UR.Land', verifyingContract: '0x8a83fbbacb82030ea17179c0403b04e7bce7ba10', version: '1', },
    message: { contents: 'Hello, Bob!', serverKey: '' } }); //dynamic message

  var from = web3.eth.accounts[0];
  var params = [from, msgParams];
  var method = 'eth_signTypedData_v4';

  web3.currentProvider.sendAsync( { method, params, from, },
    function (err, result) {
      if (err) return console.dir(err);
      if (result.error) { alert(result.error.message); }
      if (result.error) return console.error('ERROR', result);
      console.log('TYPED SIGNED:' + JSON.stringify(result.result));

      const recovered = sigUtil.recoverTypedSignature_v4({ data: JSON.parse(msgParams), sig: result.result, });

      if (ethUtil.toChecksumAddress(recovered) === ethUtil.toChecksumAddress(from)) { alert('Successfully recovered signer as ' + from); 
                                                                                     //send dynamic message and signature to server to process...
                                                                                    } 
   else {alert('Failed to verify signer when comparing ' + result + ' to ' + from); } });});
