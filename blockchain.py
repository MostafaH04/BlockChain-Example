import time
import hashlib
import json
import os
import sys

chain = []
current_transactions = []
transactions = []
transactionsLimit = 5

def proof_of_work(current_transactions):
    loading = ['|','|','|','|','/','/','/','/','-','-','-','-','-', '\\','\\','\\','\\', '|', '|', '|', '|']
    proof = 0
    loadingNum = 0
    while validify(current_transactions, proof) != True:
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

    if guessedHash[:5] == "00000":
        return True
    else:
        return False


def new_block(proof, previousHash = None,current_transactions = current_transactions
):
    block = {
        'Location in Chain': str(len(chain)+1),
        'Time': str(time.time()),
        'Proof of Work': str(proof),
        'Previous Hash': str(previousHash or hash(chain[-1])),
    }
    transactions.append(current_transactions)
    current_transactions = []
    chain.append(block)
    return block


def hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def new_transaction(sender, recipient, amount):
    current_transactions.append(
        {
            'sender':sender,
            'recipient': recipient,
            'amount': amount,
        }
    )

    return int(chain[-1]['Location in Chain'])+1


def info():
    sender = input("Sender: ")
    reciever = input("Reciever: ")
    amount = int(input("Amount: "))

    new_transaction(sender = sender, recipient = reciever, amount = amount)
    
def create():
    new_block(proof_of_work(current_transactions))
    print(f"Block #{chain[-1]['Location in Chain']} Created")



clear = lambda: os.system('cls')


new_block(proof = 100, previousHash = 1)
print(chain)

input()

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
            input()
        clear()
    elif a == 2:
        if len(current_transactions) > 0:
            create()
        else:
            print("No transcations completed yet")
            input()
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
        input()
    elif a == 5:
        exit()    
    else:
        print("Not an option")



    