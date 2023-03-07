# -*- coding: utf-8 -*-
import os
import re
import sys
import toml
import json
from web3 import Web3,HTTPProvider
      
currentDir = os.path.dirname(os.path.abspath(__file__))
config = toml.load("{}/config.toml".format(currentDir))
web3 = Web3(HTTPProvider(config["rpc"]))


fileName = config["filename"]
challangeName = config["name"]
devContract = config["dev-contract"]
flag = config["flag"]

    
with open(
    "{}/artifacts/contracts/{}/{}.json"
          .format(
              currentDir,
              fileName,
              devContract 
            )) as f:
    contract = json.load(f)
abi = contract["abi"]


def conn_handler():
    print(challangeName)
    print("")
    print("RPC: {}".format(config["rpc"]))
    print("Faucet: {}".format(config["faucet"]))
    print("\n")
    print("Option 1: Create New Contract")
    print("Option 2: Get Source Code")
    print("Option 3: Get flag by bet contract address")
    choice = None
    while choice is None:
        try:
            choice = int(input("[-] input your choice: ")) - 1
        except ValueError:
            print("must be an integer")
            continue
        else:
            if choice < 0 or choice >= 3:
                print("invalid option")
                sys.exit(1)
                
    if choice == 0:
        new_challange()
    
    elif choice == 1:
        show_source_code()
        
    elif choice == 2:
        get_flag()
        

def show_source_code():
    with open(
        "{}/contracts/{}".format(currentDir, fileName), "r"
    ) as f:
        print("\n")
        for line in f.readlines():
            print(line.split("\n")[0])
            

def new_challange():
    if os.system("cd {} && npx hardhat run --network localhost scripts/deploy.js".format(currentDir)) != 0:
        sys.exit(1)
        
        
def decrypto(ciphertext):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    import base64
    
    key = bytes.fromhex(config["key"])
    iv = bytes.fromhex(config["iv"]) 
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode("utf-8")


def get_flag():
    ciphertext = input("[-] input Your Token: ")
    try:
        tokenAddress = decrypto(ciphertext)
    except Exception as e:
        print("[+] Its' not a good token")
        sys.exit(1)
    contractAddress = input("[-] input {} address: ".format(devContract))
    if not check_address(contractAddress):
        print("[+] Its' not an address")
        sys.exit(1)
    
    if tokenAddress == contractAddress:
        print("[+] Wrong token or wrong address")
        sys.exit(1)
    
    txHash = input("[-] input tx hash that emitted 'SendFlag()' event: ")
    txReceipt = web3.eth.get_transaction_receipt(txHash)
    logs = (
            web3.eth.contract(abi=abi)
            .events["SendFlag"]()
            .processReceipt(txReceipt)
    )
    for item in logs:
        if item["address"] == contractAddress:
            print("[+] flag: {}".format(flag))
            return True
    print("[+] Sorry, you didn't get the flag")
    
    
def check_address(address: str) -> bool:
    return re.search("^0[xX][a-fA-F0-9]{40}$", address) != None

if __name__ == "__main__":
    conn_handler()
