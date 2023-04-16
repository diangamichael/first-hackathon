import hashlib
import json
import algosdk
from algosdk.v2client import algod
from beaker import sandbox


def mintNFT(algodClient, creatorAddress, creatorPrivateKey, assetName, assetUnitName):
    params = algodClient.suggested_params()
    txn = transaction.AssetConfigTxn(
        sender=creatorAddress,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name=assetUnitName,
        asset_name=assetName,
        manager=creatorAddress,
        reserve=creatorAddress,
        freeze=creatorAddress,
        clawback=creatorAddress
    )
    signed_txn = txn.sign(creatorPrivateKey)
    txid = algodClient.send_transaction(signed_txn)
    confirmed_txn = wait_for_confirmation(algodClient, txid)
    asset_id = confirmed_txn["asset-index"]
    return asset_id

def TransferNFT(algodClient, assetID, senderAddress, senderPrivateKey, receiverAddress, receiverPrivateKey):
    params = algodClient.suggested_params()
    txn = transaction.AssetTransferTxn(
        sender=senderAddress,
        sp=params,
        receiver=receiverAddress,
        amt=1,
        index=assetID
    )
    signed_txn = txn.sign(senderPrivateKey)
    txid = algodClient.send_transaction(signed_txn)
    wait_for_confirmation(algodClient, txid)
    return txid

def wait_for_confirmation(client, transaction_id):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(transaction_id)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") <= last_round):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(transaction_id)
    print(f"Transaction {transaction_id} confirmed in round {txinfo.get('confirmed-round')}")
    return txinfo