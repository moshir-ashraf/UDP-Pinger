import time
from socket import *
HOST = 'localhost'
PORT = 12000
socket = socket(AF_INET, SOCK_DGRAM)
socket.settimeout(1)
seq_num = 0
rttMin = None
rttMax = None
rttSum = 0
rttCount = 0
packetLossCount = 0

for i in range(10):
    message = input("Enter a message: ")
    seq_num += 1
    sendTime = time.time()
    message = message.encode('utf-8') + bytes([seq_num])
    socket.sendto(message, (HOST, PORT))
    try:
        message, address = socket.recvfrom(1024)
        if message.decode('utf-8'):
            if message == "Timed out".encode('utf-8'):
                print ("Server timed out and stopped.")
                break
            print ("Received Ping response from Server with Sequence Number",message[-1])
            receiveTime = time.time()
            rtt = receiveTime - sendTime
            if rttMin is None or rtt < rttMin:
                rttMin = rtt
            if rttMax is None or rtt > rttMax:
                rttMax = rtt
            rttSum += rtt
            rttCount += 1
            print(' RTT: ' + str(round(rtt, 6)) + ' seconds')
    except timeout:
            print ("Request timed out")
            packetLossCount += 1

if rttCount > 0:
    rttAvg = rttSum / rttCount
else:
    rttAvg = 0

packetLossRate = (packetLossCount / 10) * 100

print('--- Ping statistics ---')
print(str(rttCount) + ' packets transmitted, ' + str(rttCount - packetLossCount) + ' received, '
      + str(packetLossRate) + '% packet loss')
if rttCount > 0:
    print('Minimum RTT:', rttMin, 'seconds')
    print('Maximum RTT:', rttMax, 'seconds')
    print('Average RTT:', rttAvg, 'seconds')
else:
    print('No RTT measurements')

      