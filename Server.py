from socket import * 
PORT = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM) 
serverSocket.bind(('', PORT))
serverSocket.settimeout(10)
last_seq_num = 0
lost_packets = []
temp = ''
print('The server is ready to receive')
print('Server is listening for client heartbeats...')
while True:   
    try:
         message,address = serverSocket.recvfrom(1024)
         temp = address
         if message.decode('utf-8'):
             seq_num = message[-1]
             if seq_num != last_seq_num + 1:
               print(f"Packet loss detected between sequence numbers {last_seq_num} and {seq_num}")
               lost_packets += list(range(last_seq_num, seq_num))
             else:
               print("Received Ping Request from Client with Sequence Number",seq_num,"and value \'",message.decode('utf-8')[:-1],"\'")
             last_seq_num = seq_num 
    except timeout:
        print("Server timed out and stopped.")
        newmsg = 'Timed out'.encode('utf-8')
        serverSocket.sendto(newmsg, temp)
        break
    message = 'Ping'.encode('utf-8') + bytes([seq_num])
    serverSocket.sendto(message, address)
if lost_packets:
    print('Packets lost:', lost_packets)
else:
    print('No packets lost')
