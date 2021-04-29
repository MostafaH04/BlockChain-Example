import time
import hashlib
import json
import os
import sys

chain = []

with open("chain.txt") as f:
    chain = [line.rstrip() for line in f]

f.close()

global current_transactions
current_transactions = []
transactions = [{None}]
transactionsLimit = 5

def proof_of_work(current_transactions):
    loading = ['|','|','|','|','/','/','/','/','-','-','-','-','-', '\\','\\','\\','\\', '|', '|', '|', '|']
    proof = 0
    loadingNum = 0
    while True:
        if validify(current_transactions, proof) is True:
            break
        if loadingNum < len(loading)-1:
            loadingNum += 1
        else:
            loadingNum = 0
        
        sys.stdout.write("\rMining "+ loading[loadingNum])
        sys.stdout.flush()
        sys.stdout.write('\b')
        #time.sleep(0.1)
        proof +=1
    
    return proof

def validify(current_transactions, proof):
    guessedHash = hashlib.sha256(f'{current_transactions}{proof}'.encode()).hexdigest()
    if guessedHash[:4] == "0000":
        return True
    else:
        return False


def new_block(proof, previousHash = None):
    block = {
        'Location in Chain': str(len(chain)+1),
        'Time': str(time.time()),
        'Proof of Work': str(proof),
        'Transactions': str(current_transactions),
        'Previous Hash': str(previousHash or hash(chain[-1]['Transactions'],int(chain[-1]['Proof of Work']))),
    }
    transactions.append(current_transactions)
    current_transactions.clear()
    chain.append(block)
    return block


def hash(transaction, proof):
    new = hashlib.sha256(f'{transaction}{proof}'.encode()).hexdigest()
    return new

def new_transaction(sender, recipient, amount):
    current_transactions.append(
        {
            'sender':sender,
            'recipient': recipient,
            'amount': amount,
        }
    )



def info():
    sender = input("Sender: ")
    reciever = input("Reciever: ")
    amount = int(input("Amount: "))

    new_transaction(sender = sender, recipient = reciever, amount = amount)
    
def create():
    new_block(proof_of_work(current_transactions))
    print(f"Block #{chain[-1]['Location in Chain']} Created")
    input("\n\n\nPress Enter To Continue")



clear = lambda: os.system('cls')



print(chain)

input("\n\n\nPress Enter To Continue")

while True:
    clear = lambda: os.system('cls')
    clear()
    
    for i in chain:
        print(i)
    print(['1 - New Transaction','2 - New Block', '3 - Reset Chain','4 - View Transactions', '5 - Exit'])
    a = int(input("#: "))
    
    if a == 1:
        if len(current_transactions) < transactionsLimit:
            info()
        else:
            print("Block transaction limit met, creating new block. Try again after")
            create()
            input("\n\n\nPress Enter To Continue")
        clear()
    elif a == 2:
        if len(current_transactions) > 0:
            create()
        else:
            print("No transcations completed yet")
            input("\n\n\nPress Enter To Continue")

        clear()

    elif a == 3:
        chain = []
        new_block(proof = 100,previousHash = 1)
        clear()
    elif a == 4:
        clear()
        for i in chain:
            print(i)

        print("\n\n\n")

        b = int(input("Block Number: "))

        if b != 1:
            for i in transactions[b-1]:
                print(i)
        else:
            print("Initial Block - No transactions")
        input("\n\n\nPress Enter To Continue")
    elif a == 5:
        
        f = open("chain.txt", "w")
        for i in chain:
            f.write(i+"\n")

        f.close()

        exit()
    else:
        print("Not an option")
        input("\n\n\nPress Enter To Continue")



    