Requirements
- install redis server
- install redis python client using pip install redis



Usage
- You can just import Queue from createQueue then pass queue number and phone number to add to queue like Queue().addNumberToQueue(queue, number)
- Number should be passed as your PBX outbound routes expect it to be i.e with country code or not etc
- change context in configurations.ini, if your PBX queues are not under ext-queues context