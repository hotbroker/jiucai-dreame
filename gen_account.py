# -*- coding:utf-8 -*-
import json
import os
import subprocess
import sys
import sys
import logging
import time

import requests
import web3.eth

import utils
import traceback
import logging.handlers
from web3 import Web3
from mnemonic import Mnemonic

import uuid

def create_accounts(cnt):
    accounts_list=[]
    idx=0
    while cnt>0:
        cnt=cnt-1
        idx = idx+1
        randid = uuid.uuid4().hex + uuid.uuid4().hex

        from eth_account import Account
        acct = Account.create(randid)
        accounts_list.append({'idx':idx, 'addr':acct.address,"key":acct.key.hex()})
    filename="accounts_" + utils.time_to_string_filename(time.time())+".txt"
    open(filename, "w").write(json.dumps(accounts_list,indent=4))
    print("result: {}".format(filename))



def create_mnemonic(cnt):
    '''
    创建账号，带且助记词
    :param cnt:需要生成多少个
    :return:
    '''
    mnemo = Mnemonic("english")
    accounts_list=[]
    idx=0
    for i in range(cnt):
        idx=idx+1
        words = mnemo.generate(strength=256)
        addr=utils.words_to_addr(words)
        key = utils.words_to_prikey(words)

        accounts_list.append({'idx': idx, 'addr': addr, "key": key,"mnemonic":words})
    filename = "mnemonic_accounts_" + utils.time_to_string_filename(time.time()) + ".txt"

    open(filename, "w").write(json.dumps(accounts_list,indent=4))
    print("result: {}".format(filename))


if __name__=="__main__":
    create_mnemonic(10)
    create_accounts(10)