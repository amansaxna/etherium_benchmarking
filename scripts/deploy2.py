from brownie import accounts, config, Records_Keeper, network, chain, web3
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy


import time
import matplotlib.pyplot as plt
import numpy as np

class bcolors:
    GREEN = '\033[92m' #GREEN
    YELLOW = '\033[93m' #YELLOW
    RED = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR


gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

gas_price(gas_strategy)



def deploy_hc():
    print(web3.eth.gasPrice)
    print(chain.time())
    global account
    account = get_account()
    #print(dir(account))
    global records_keeper
    records_keeper = Records_Keeper.deploy( {"from": account} )
    print(bcolors.YELLOW + "Contact deployedSuccessfully!" ) #+ bcolors.RESET

# Transaction latency (confirmation_time - submission_time)
def add_treatment(iter):
    #checking the transaction latency for adding 1 treatment
    # time start 
    #print(chain.height)
    while(iter != 0):
        start1 = time.time()
        transaction = records_keeper.addTreatment("d1","t1","m1", {"from": account})
        '''
        ,"required_confs" : 1
        '''
        start = time.time()

        print(dir(transaction))
        web3.eth.wait_for_transaction_receipt(transaction.txid, timeout=120, poll_latency=0.1)
        end = time.time()
        print("time elapsed {} milli seconds".format((end-start)*1000))
        print("time elapsed {} milli seconds".format((end-start1)*1000))
        print("time elapsed {} milli seconds".format((start1-start)*1000))

        while(not web3.eth.wait_for_transaction_receipt(transaction.txid, timeout=120, poll_latency=0.1)):
            print(".")
        print("block_number",transaction.block_number)
        block = web3.eth.get_block(transaction.block_number)
        #block_1 = web3.eth.get_block(transaction.block_number -1 )
        print(block.timestamp)
        #print(block_1.timestamp)
        print(transaction.confirmations)
        print("events", transaction.events)
        print("function name", transaction.fn_name)
        print("modified_state", transaction.modified_state)
        transaction.wait(1) # wait for 2 confirmation

        iter = iter - 1

    #transaction.wait(1)
    ''''
    print(chain.time())
    print(chain.height)
    print(transaction.timestamp)
    

    transaction = records_keeper.addTreatment("d1","t1","m1", {"from": account})
    
    print("status",transaction.status)
    print("Timestamp",transaction.timestamp)
    print("block_number",transaction.block_number)
    print("confirmations",transaction.confirmations)
    print("status",transaction.status)
    '''

# Read latency (available_time - submission_time)
def view_history(iter):
    while(iter != 0):
        transaction = records_keeper.viewHistory( {"from": account} )
        #web3.eth.wait_for_transaction_receipt(transaction.txid, timeout=120, poll_latency=0.1)
        print(transaction)
        #print(dir(transaction))

        #print("modified_state", transaction.modified_state)
        iter = iter - 1
def get_account():
    if network.show_active() == "development":
        #priority_fee("2 gwei")
        return accounts[2]
    else:
        return accounts.add(config["wallets"]["from_key"])

def trans_latency_view_history():
    no_transaction = [1,50,100,150]
    no_transaction_half = [1,50]
    time_taken = []
    time_taken_read = []

    start = time.time()
    add_treatment(1)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken.append((end-start)*1000)

    #-----------------------------------------------------
    start = time.time()
    view_history(1)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken_read.append((end-start)*1000)
    
    
    
    start = time.time()
    add_treatment(50)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken.append((end-start)*1000)

    #-----------------------------------------------------
    start = time.time()
    view_history(1)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken_read.append((end-start)*1000)
    

    start = time.time()
    add_treatment(100)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken.append((end-start)*1000)

    #-----------------------------------------------------
    start = time.time()
    view_history(1)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken_read.append((end-start)*1000)
    
    start = time.time()
    add_treatment(150)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken.append((end-start)*1000)

    #-----------------------------------------------------
    start = time.time()
    view_history(1)
    end = time.time()
    print("time elapsed {} milli seconds".format((end-start)*1000))
    time_taken_read.append((end-start)*1000)

'''
    print(time_taken)
    print(time_taken_read)
    xpoints = np.array(no_transaction_half)
    ypoints = np.array(time_taken)
    plt.plot(xpoints, ypoints)
    plt.savefig("mygraph.png")
    plt.show()

    plt.bar(xpoints, ypoints)
    plt.savefig("write_latency_graph.png")


    xpoints = np.array(no_transaction_half)
    ypoints = np.array(time_taken_read)
    plt.plot(xpoints, ypoints)
    plt.savefig("read_latency_graph.png")
    plt.show()
    
'''
def main():
    deploy_hc()
    trans_latency_view_history()
    view_history(1)
    

    


 


 