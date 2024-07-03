import socket
import configparser
import time

class Socket:
    def __init__(self):
        configs = configparser.ConfigParser()
        configs.read('configurations.ini')
        self.amiserver = configs['settings']['amiserver']
        self.amiport = configs['settings']['amiport']
        self.amiuser = configs['settings']['amiuser']
        self.amipassword = configs['settings']['amipassword']
        self.context = configs['settings']['context']
        self.exten = configs['settings']['exten']
    
    def establishConnection(self):
        self.socket = socket.create_connection((self.amiserver, self.amiport))
        events = "originate,call"
        authenticationRequest = (
            "Action: Login\r\n"
            f"Username: {self.amiuser}\r\n"
            f"Secret: {self.amipassword}\r\n"
            f"Events: {events}\r\n\r\n"
        )
        self.socket.sendall(authenticationRequest.encode())
        time.sleep(0.2)
        try:
            response = self.socket.recv(4096).decode()
            if 'Success' in response:
                status = "Connected"
            else:
                status = "Could not authenticate"              
        except self.socket.timeout:
            status = "Socket send timed out"
        except self.socket.error as e:
            status = f"Socket send error: {e}"
        return status
    

    def initiateCall(self, queue, number, sales = "FALSE", closed="FALSE"):
        mychannel = f"Local/{number}@from-internal"
        if self.exten == "Queue":
            self.exten = queue
        originateRequest = (
            "Action: Originate\r\n"
            f"Channel: {mychannel}\r\n"
            f"Variable: clid={number}\r\n"
            f"Variable: GOTO_SALES={sales}\r\n"
            f"Variable: CLOSED={closed}\r\n"
            f"Variable: ROUTER_QUEUE={queue}\r\n"
            "Callerid: \r\n"
            f"Exten: {self.exten}\r\n"
            f"Context: {self.context}\r\n"
            "Priority: 1\r\n"
            "Async: true\r\n\r\n"
                )
        
        self.socket.sendall(originateRequest.encode())
        time.sleep(1)
    
    def checkCallStatus(self, number):
        call_answered = False
        orignateResponse = self.socket.recv(4096).decode()
        print(orignateResponse)
        if "Success" in orignateResponse:
            stop = False
            while True:
                Responses = self.socket.recv(4096).decode().split("\r\n")
                for response in Responses:
                    print(response)
                    # Check for NewState or Bridge events indicating the call was answered
                    if "ChannelStateDesc: Up" in response and number in response:
                        call_answered = True
                        print("Call was answered")
                        stop = True
                        break
                    if "OriginateResponse" in response and number in response:
                        print("Call initiated but not answered by customer")
                        stop = True
                        break
                if stop is True:
                    break
        return call_answered
    
    def checkAvailableAgents(self, queue):
        queueRequest = (
            "Action: QueueSummary\r\n"
            f"Queue: {queue}\r\n\r\n"
        )
        self.socket.sendall(queueRequest.encode())
        time.sleep(0.5)
        queueResponse = self.socket.recv(4096).decode().split("\r\n\r\n")
        howManyToCall = 0
        for response in queueResponse:
            if "Event: QueueSummary" in response:
                #print(response)
                queueSummary = response.split("\r\n")
                for line in queueSummary:
                    if "Available:" in line:
                        line = line.split(":")
                        agents = int(line[1].strip())
                    if "Callers:" in line:
                        line = line.split(":")
                        calls = int(line[1].strip())
                if agents > calls:
                    howManyToCall = agents - calls
        return howManyToCall

oursocket = Socket()
oursocket.establishConnection()
oursocket.checkAvailableAgents(211)