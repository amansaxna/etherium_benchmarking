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

# Read latency (available_time - submission_time)
def view_history(iter):
    while(iter != 0):
        transaction = records_keeper.viewHistory( {"from": account} )
        #web3.eth.wait_for_transaction_receipt(transaction.txid, timeout=120, poll_latency=0.1)
        #print(transaction)
        #print(dir(transaction))

        #print("modified_state", transaction.modified_state)
        iter = iter - 1
def get_account():
    if network.show_active() == "development":
        #priority_fee("2 gwei")
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

# Transaction latency (confirmation_time - submission_time)
def add_treatment(iter):
    transactions = set()#{ "transactions" }
    while(iter != 0):
        start1 = time.time()
        trans = records_keeper.addTreatment("d1","t1","m1", {"from": account})
        #transactions["transactions"].add(trans)
        transactions.add(trans)
        #print(transactions)
        '''
        ,"required_confs" : 1
        '''
        #transaction.wait(1) 

        iter = iter - 1

    for transaction in transactions:
        web3.eth.wait_for_transaction_receipt(transaction.txid, timeout=120, poll_latency=0.1)

        block = web3.eth.get_block(transaction.block_number)

    #transaction.wait(1)


def trans_latency_view_history(no_transaction):
    #no_transaction = [1,50,100,200,400]
    #no_transaction_half = [1,50]

    time_taken = []
    time_taken_read = []
    throughput_write = []
    throughput_read = []

    for i in no_transaction:
        start = time.time()
        add_treatment(i)
        end = time.time()
        #print("time elapsed {} milli seconds".format((end-start)*1000))
        time_taken.append((end-start)*1000)
        throughput_i =  i / (end-start)*1000
        throughput_write.append(throughput_i)

        #-----------------------------------------------------
        start = time.time()
        view_history(1)
        end = time.time()
        #print("time elapsed {} milli seconds".format((end-start)*1000))
        time_taken_read.append((end-start)*1000)

        throughput_i =  i / (end-start)*1000
        throughput_read.append(throughput_i)
    
    print(time_taken)
    print(time_taken_read)
    print(throughput_write)
    print(throughput_read)

    xpoints = np.array(no_transaction)
    ypoints = np.array(time_taken)
    plt.plot(xpoints, ypoints)
    plt.savefig("mygraph.png")
    plt.show()
    plt.xlabel("no_transaction")
    plt.ylabel("time_taken_write")
    plt.title("TL")
    #plt.bar(xpoints, ypoints)
    plt.grid()
    plt.savefig("write_latency_graph_test.png")


    xpoints = np.array(no_transaction)
    ypoints = np.array(time_taken_read)

    plt.plot(xpoints, ypoints)
    plt.xlabel("no_transaction")
    plt.ylabel("time_taken_read")
    plt.title("RL")
    plt.grid()
    plt.savefig("read_latency_graph_test.png")
    plt.show()

    #+------------------------------------------
    xpoints = np.array(no_transaction)
    ypoints = np.array(throughput_write)

    plt.plot(xpoints, ypoints)
    plt.xlabel("no_transaction")
    plt.ylabel("throughput_write")
    plt.title("RL")
    plt.grid()
    plt.savefig("throughput_write_graph_test.png")
    plt.show()

    #+------------------------------------------
    xpoints = np.array(no_transaction)
    ypoints = np.array(throughput_read)

    plt.plot(xpoints, ypoints)
    plt.xlabel("no_transaction")
    plt.ylabel("throughput_read_test")
    plt.title("RL")
    plt.grid()
    plt.savefig("throughput_read_graph_test.png")
    plt.show()

def main():
    deploy_hc()
    #no_transaction = [1,50,100,200,400,800,1600]
    no_transaction = [1,50,100,200]
    trans_latency_view_history(no_transaction)
    view_history(1)
    

    


 