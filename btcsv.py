#!/usr/bin/env python3
# coding=utf8

from hashlib import sha256
import re
import sys
import os
import threading
import secrets
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

def randomforkey():
    # Generate a random private key for Bitcoin SV
    return secrets.randbits(256)

def compute_adr(priv_num):
    # Generate a Bitcoin SV address from the private key
    secret = CBitcoinSecret.from_secret_bytes(priv_num.to_bytes(32, 'big'))
    address = P2PKHBitcoinAddress.from_pubkey(secret.pub)
    return str(address)

def create_rainbow_table(num_addresses):
    # Generate a rainbow table of Bitcoin SV addresses
    rainbow_table = set()
    for _ in range(num_addresses):
        privkeynum = randomforkey()
        address = compute_adr(privkeynum)
        rainbow_table.add(address)
    return rainbow_table

def search_for_collision(target_address, rainbow_table):
    wallets = 0
    collision_found = False

    while not collision_found:
        privkeynum = randomforkey()
        address = compute_adr(privkeynum)

        if address in rainbow_table:
            collision_found = True
        else:
            wallets += 1

        if wallets % 1000 == 0:
            print('\r' + 'Searched ', wallets, ' addresses', end='', flush=True)

    print('Wallet Found!')
    print("\nAddress :  %s \n" % address)
    print("PrivKey :  %s\n" % privkeynum)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        # Updated regular expression for BSV addresses
        assert re.match(r"^q[1-9A-HJ-NP-Za-km-z]{42}$", arg1) is not None
        searchstring = arg1.lower()
        listwide = 4 * os.cpu_count() * 2 ** len(searchstring)
        vanity = True
    else:
        print("Please specify a target address as an argument.")
        sys.exit(1)

    num_addresses = 1000000  # Adjust this number to increase the chances of collision
    rainbow_table = create_rainbow_table(num_addresses)
    search_for_collision(searchstring, rainbow_table)
