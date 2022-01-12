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

_bsc_rpc='https://bsc-dataseed.binance.org/'
_bsc_testnet='https://data-seed-prebsc-1-s1.binance.org:8545'
#_bsc_rpc=_bsc_testnet

w3=w3obj  = Web3(Web3.HTTPProvider(_bsc_rpc))


def send_amount(from_prikey, to, sendvalue, tokenobj):
    account_key = from_prikey
    w3=w3obj
    acct = w3.eth.account.privateKeyToAccount(account_key)
    addr = acct.address

    gasprice = w3.toWei('5', 'gwei')
    print('gasprice', gasprice)
    print('sendvalue', sendvalue)
    decimals = int(tokenobj.functions.decimals().call())
    print('decimals', decimals)
    sendvalue = utils.get_18_num(sendvalue, decimals)

    nonce_online = w3obj.eth.get_transaction_count(acct.address)
    trans = tokenobj.functions.transfer(to, sendvalue).buildTransaction({
        'nonce': nonce_online,
        'gasPrice': gasprice,
        'gas': 200000,
        'chainId': w3obj.eth.chain_id

    })


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

def send_to_accounts(key, toaccounts, sendamount, token) -> None:
    n = 0
    sendamount = float(sendamount)
    src = w3.eth.account.privateKeyToAccount(key)
    srcaddr = src.address
    print('sender:', srcaddr)
    print('to account number:', len(toaccounts))
    print('sendamount:', sendamount)
    tokenabi = json.load(open('BSC_USDC.abi'))

    tokenobj = w3.eth.contract(address=Web3.toChecksumAddress(token), abi=tokenabi)

    for to_addr in toaccounts:
        n = n + 1
        logging.info("{}/{})acc:{}".format(n, len(toaccounts), to_addr))

        nonce_online1 = w3.eth.get_transaction_count(srcaddr)
        send_amount(key, to_addr, sendamount,tokenobj)

        nonce_online2 = w3.eth.get_transaction_count(srcaddr)
        while nonce_online2 == nonce_online1:
            nonce_online2 = w3.eth.get_transaction_count(srcaddr)
            time.sleep(1)
            print("wait trans confirm {},{}, to {}".format(nonce_online2, nonce_online1, to_addr))

        new_balance = w3.eth.getBalance(to_addr)
        print('acc', to_addr, 'balance', new_balance)
        print('\n\n\n')


def go():
    if len(sys.argv)!=5:
        print(sys.argv)
        fname = os.path.basename(os.path.abspath(__file__))
        logging.info('missing parmeters')
        logging.info('usage:python {} src_privite_key to_account_list_filename amount tokenaddress'.format(fname))
        logging.info('usage:python {} 0x11111111111111111111 myaccounts.json 0.01 tokenaddress'.format(fname))
        return

    srckey = sys.argv[1]
    tolist=[]
    buf = open(sys.argv[2]).read()
    tolist1 = json.loads(buf)
    for k in tolist1:
        tolist.append(k['addr'])
    sendvalue = float(sys.argv[3])
    token = sys.argv[4]
    send_to_accounts(srckey, tolist, sendvalue, token)

if '__main__'==__name__:
    fname = os.path.basename(os.path.abspath(__file__))
    utils.init_log("{}.log".format(fname))
    go()
