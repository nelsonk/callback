import threading
import sys
from QueueManagement import Queue
from socketManagement import Socket
import time

queuelist = [100, 101]

def call(queuePassed, retry=0):
    ourSocket = Socket()
    while True:
        socketStatus = ourSocket.establishConnection()
        if socketStatus == "Connected":
            howManyToCall = ourSocket.checkAvailableAgents(queuePassed)
            print(f"How many to call: {howManyToCall}")
            if howManyToCall > 0:
                numbers = queue.getNumberFromQueue(queuePassed, howManyToCall)
                if numbers == None:
                    print(f"All numbers for Queue {queuePassed} have been called")
                else:
                    for number in numbers:
                        ourSocket.initiateCall(queuePassed, number)
                        status = ourSocket.checkCallStatus(number) #This waits for call to be picked or to hangup for no need for sleep before trying another number
                        if status is True:
                            print("Successful")
                        else:
                            print(f"Failed, adding number {number} back to queue")
                            queue.addNumberToQueue(queuePassed, number)
        else:
            if retry > 1:
                print("Failed to connect to AMI server")
            return call(queuePassed, retry + 1)
        ourSocket.socket.close()


if __name__ == "__main__":
    queue = Queue()
    if len(sys.argv) > 2:
        try:
            ourQueue = sys.argv[1]
            phoneNumber = sys.argv[2]
            queue.addNumberToQueue(ourQueue, phoneNumber)
        except Exception as e:
            print(f"Exception {e} occured while adding number to queue")
    else:    
        for q in queuelist:           
            callThread = threading.Thread(target=call, args=(q,))
            callThread.start()
                