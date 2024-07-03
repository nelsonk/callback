import redis


class Queue:
    def __init__(self):
        self.conn = redis.Redis(host="localhost", port=6379, db=0)

    def addNumberToQueue(self, queue, number):
        result = self.conn.rpush(queue, number)
        return f"Successfully added, now Queue {queue} has {result} numbers"

    def getNumberFromQueue(self, queue, limit):
        number = self.conn.lpop(queue, limit)
        if number is not None:
            if not isinstance(number, list):
                number = list(number.decode())
        yield number
    
