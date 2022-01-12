# -*- coding:utf-8 -*-
import json
import os
import subprocess
import sys
import sys
import logging
import time

import traceback
from web3 import Web3
from web3.auto import w3

import utils

_bsc_rpc='https://rpc-mainnet.maticvigil.com'

w3=w3obj  = Web3(Web3.HTTPProvider(_bsc_rpc))


def send_amount(from_prikey, to, sendvalue):
    account_key = from_prikey
    w3=w3obj
    acct = w3.eth.account.privateKeyToAccount(account_key)
    addr = acct.address

    gasprice = w3.toWei('30', 'gwei')
    print('gasprice', gasprice)
    print('sendvalue', sendvalue)
    sendvalue = utils.get_18_num(sendvalue)

    nonce_online = w3obj.eth.get_transaction_count(acct.address)

    trans = {
        'nonce': nonce_online,
        'gasPrice': gasprice,
        'gas': 22000,
        'chainId': w3obj.eth.chain_id,
        'value': sendvalue,
        'to': to
    }

    logging.info('trans info ' + str(trans))
    signed_txn = w3.eth.account.sign_transaction(trans, private_key=account_key)
    txhash = signed_txn.hash.hex()
    logging.info("trxhash:" + txhash)

    sendres = ""
    while 1:
        try:
            sendres = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        except ValueError as ex:
            print('ex', ex)
            print('typeex', type(ex))
            if str(ex).find('nonce too low') != -1 or str(ex).find('already known') != -1:
                break
            else:
                continue

    try:
        waitres = w3.eth.wait_for_transaction_receipt(sendres.hex())
        print("send succ")
        return
    except:
        print("wait time out")
        strexct = "except {}".format(traceback.format_exc())
        print(strexct)

def send_to_accounts(key, toaccounts, sendamount) -> None:
    n = 0
    sendamount = float(sendamount)
    src = w3.eth.account.privateKeyToAccount(key)
    srcaddr = src.address
    print('sender:', srcaddr)
    print('to account number:', len(toaccounts))
    print('sendamount:', sendamount)

    for to_addr in toaccounts:
        n = n + 1
        logging.info("{}/{})acc:{}".format(n, len(toaccounts), to_addr))

        nonce_online1 = w3.eth.get_transaction_count(srcaddr)
        send_amount(key, to_addr, sendamount)

        nonce_online2 = w3.eth.get_transaction_count(srcaddr)
        while nonce_online2 == nonce_online1:
            nonce_online2 = w3.eth.get_transaction_count(srcaddr)
            time.sleep(1)
            print("wait trans confirm {},{}, to {}".format(nonce_online2, nonce_online1, to_addr))

        new_balance = w3.eth.getBalance(to_addr)
        print('acc', to_addr, 'balance', new_balance)
        print('\n\n\n')


def go():
    if len(sys.argv)!=4:
        logging.info('missing parmeters')
        logging.info('usage:python transfer_bsc.py src_privite_key to_account_list_filename amount')
        logging.info('usage:python transfer_bsc.py 0x11111111111111111111 myaccounts.json 0.01')
        return
    srckey = sys.argv[1]

    tolist=utils.get_to_address(sys.argv[2])
    sendvalue = float(sys.argv[3])

    send_to_accounts(srckey, tolist, sendvalue)

if '__main__'==__name__:
    utils.init_log("transfer_bsc.log")
    go()
