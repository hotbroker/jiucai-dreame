# -*- coding:utf-8 -*-
import json
import os
import subprocess
import sys
from web3 import Web3
import logging.handlers
import mnemonic_utils
from web3.auto import w3
import  datetime
from datetime import datetime

def init_log(logfile='jiucai-dream.log'):
    logging.getLogger().setLevel(logging.NOTSET)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    logging.getLogger('web3.providers.HTTPProvider').setLevel(logging.WARNING)
    logging.getLogger('web3.RequestManager').setLevel(logging.WARNING)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    h1 = logging.StreamHandler(sys.stdout)
    h1.setFormatter(formatter)
    h1.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(h1)
    h2 = logging.handlers.RotatingFileHandler(
        filename=logfile, maxBytes=(1048576 * 5), backupCount=7
    )
    h2.setFormatter(formatter)
    h2.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(h2)

def privkey_to_account(key):
    acc = w3.eth.account.privateKeyToAccount(key)
    return acc.address

def words_to_prikey(words):
    private_key = mnemonic_utils.mnemonic_to_private_key(
        words, str_derivation_path=f'{mnemonic_utils.LEDGER_ETH_DERIVATION_PATH}/0')
    return private_key.hex()

def words_to_addr(words):
    r = words_to_prikey(words)
    return privkey_to_account(r)


def time_to_string(timestamp1):
    return datetime.fromtimestamp(timestamp1).strftime("%Y-%m-%d, %H:%M:%S")

def time_to_string_filename(timestamp1):
    return datetime.fromtimestamp(timestamp1).strftime("%Y_%m_%d %H_%M_%S")

