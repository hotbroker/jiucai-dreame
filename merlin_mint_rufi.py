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
import threading

_bsc_rpc='https://rpc.merlinchain.io'


w3=w3obj  = Web3(Web3.HTTPProvider(_bsc_rpc))
chain_id = w3obj.eth.chain_id

gasprice = w3.toWei('0.1', 'gwei')


def send_amount(from_prikey, to, sendvalue, tokenobj, nonce_online):
    
    account_key = from_prikey
    w3=w3obj
    acct = w3.eth.account.privateKeyToAccount(account_key)
    addr = acct.address

    print('gasprice', gasprice)

    trans = tokenobj.functions.transfer(addr, sendvalue).buildTransaction({
        'nonce': nonce_online,
        'gasPrice': gasprice,
        'gas': 100000,
        'chainId': chain_id

    })

    trans['data']='0x40c10f190000000000000000000000009bd60d6fc99843207b8149f9190438c1f81bddcd0000000000000000000000000000000000000000000000000000000000000014'
    logging.info('trans info ' + str(trans))
    signed_txn = w3.eth.account.sign_transaction(trans, private_key=account_key)
    txhash = signed_txn.hash.hex()
    logging.info("trxhash:" + txhash)

    sendres = ""
    while 1:
        try:
            print('send raw')
            #call send_raw_transaction with new thread

            def send_raw_transaction_thread(signed_txn):
                global sendres
                sendres = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            thread = threading.Thread(target=send_raw_transaction_thread, args=(signed_txn,))
            thread.start()
            #thread.join()
            print('sendres', sendres)
            break


        except ValueError as ex:
            print('ex', ex)
            print('typeex', type(ex))
            if str(ex).find('nonce too low') != -1 or str(ex).find('already known') != -1:
                break
            else:
                continue

    try:
        #waitres = w3.eth.wait_for_transaction_receipt(sendres.hex())
        print("send succ")
        
        return
    except:
        print("wait time out")
        strexct = "except {}".format(traceback.format_exc())
        print(strexct)

def send_to_accounts(key,  number, mincontract) -> None:
    n = 0
    sendamount = 0
    src = w3.eth.account.privateKeyToAccount(key)
    srcaddr = src.address
    print('sender:', srcaddr)
    
    tokenabi = json.load(open('BSC_USDC.abi'))
    token = '0x9bd60d6FC99843207B8149f9190438C1F81BDdcD'
    tokenobj = w3.eth.contract(address=Web3.toChecksumAddress(token), abi=tokenabi)
    
    bal = tokenobj.functions.balanceOf(srcaddr).call()
    logging.info(f'{srcaddr} balance:{bal/10**18}')
    if bal/10**18>500000:
        logging.info('balance is enough')
        return True

    tokenobj = w3.eth.contract(address=Web3.toChecksumAddress(mincontract), abi=tokenabi)
    nonce_online1 = w3.eth.get_transaction_count(srcaddr)
    print('nonce_online1', nonce_online1)
    for to_addr in range(0, number):
        n = n + 1
        logging.info("{}/{})acc:{}".format(n, number, to_addr))

        send_amount(key, to_addr, sendamount,tokenobj, nonce_online1)
        nonce_online1 = nonce_online1+1
        time.sleep(1)

        print('\n\n\n')



def go():
    if len(sys.argv)!=3:
        print(sys.argv)
        fname = os.path.basename(os.path.abspath(__file__))
        logging.info('missing parmeters')
        logging.info('usage:python {} src_privite_key number'.format(fname) )
        logging.info('usage:python {} 0x11111111111111111111 10 '.format(fname))
        return

    srckey = sys.argv[1]
    
    number=int(sys.argv[2])

    mincontracttoken = '0xC47b6F403C03B5223140DD439C8Ba04bF520a170'
    
    while 1:
        r = send_to_accounts(srckey, number, mincontracttoken)
        if r:
            print('send finished')
            break
        time.sleep(10)

if '__main__'==__name__:
    fname = os.path.basename(os.path.abspath(__file__))
    utils.init_log("{}.log".format(fname))
    go()
