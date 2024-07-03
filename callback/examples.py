queue = Queue()
queue.addNumberToQueue(100, "0779564427")
queue.addNumberToQueue(100, "0704453873")
print(queue.getNumberFromQueue(100))

testSocket = Socket()
testSocket.establishConnection()
testSocket.initiateCall("211", "0779564427")
print(testSocket.checkCallStatus("0779564427"))