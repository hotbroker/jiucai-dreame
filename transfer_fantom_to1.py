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

w3=w3obj  = Web3(Web3.HTTPProvider('https://rpc.ftm.tools'))


_GAS_PRICE=500

def send_amount(from_prikey, to, sendvalue):
    account_key = from_prikey
    w3=w3obj
    acct = w3.eth.account.privateKeyToAccount(account_key)
    addr = acct.address

    gasprice = w3.toWei(_GAS_PRICE, 'gwei')
    print('gasprice', gasprice)
    print('sendvalue', sendvalue)
    sendvalue = utils.get_18_num(sendvalue)

    nonce_online = w3obj.eth.get_transaction_count(acct.address)

    trans = {
        'nonce': nonce_online,
        'gasPrice': gasprice,
        'gas': 25000,
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
            if str(ex).find('transaction underpriced')!=-1:
                logging.error('gas to low to make a transation!!')
                return
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


def accounts_to_one(accounts, targetaccount, sendamount) -> None:
    n = 0
    sendamount = float(sendamount)

    print('sendamount:', sendamount)

    for src_key in accounts:
        n = n + 1
        src = w3.eth.account.privateKeyToAccount(src_key)
        srcaddr = src.address
        srcbalance = w3obj.eth.getBalance(srcaddr)
        logging.info("{}/{})acc:{}, balance:{:.5}".format(n, len(accounts), srcaddr, srcbalance/(10**18)))

        nonce_online1 = w3.eth.get_transaction_count(srcaddr)
        send_amount(src_key, targetaccount, sendamount)

        nonce_online2 = w3.eth.get_transaction_count(srcaddr)
        while nonce_online2 == nonce_online1:
            nonce_online2 = w3.eth.get_transaction_count(srcaddr)
            time.sleep(1)
            print("wait trans confirm {},{}, to {}".format(nonce_online2, nonce_online1, srcaddr))

        new_balance = w3.eth.getBalance(targetaccount)
        print('acc', targetaccount, 'balance', new_balance)
        print('\n\n\n')



def go():
    if len(sys.argv)!=4:
        logging.info('missing parmeters')
        logging.info('usage:python transfer_fantom_to1.py src_key_list_filename to_account_addr amount')
        return
    srckeyfile = sys.argv[1]
    src_key_list = utils.get_file_to_lines(srckeyfile)
    to_account_addr = sys.argv[2]
    sendvalue = float(sys.argv[3])

    accounts_to_one(src_key_list, to_account_addr, sendvalue)

if '__main__'==__name__:
    utils.init_log("transfer_fantom_to1.log")
    go()
