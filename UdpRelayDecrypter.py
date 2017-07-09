import sys, socket
from simplecrypt import encrypt, decrypt


def fail(reason):
    sys.stderr.write(reason + '\n')
    sys.exit(1)


if len(sys.argv) != 2 or len(sys.argv[1].split(':')) != 3:
    fail('Usage: udp-relay.py localPort:remoteHost:remotePort')

localPort, remoteHost, remotePort = sys.argv[1].split(':')

try:
    localPort = int(localPort)
except:
    fail('Invalid port number: ' + str(localPort))
try:
    remotePort = int(remotePort)
except:
    fail('Invalid port number: ' + str(remotePort))

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', localPort))
except:
    fail('Failed to bind on port ' + str(localPort))

knownClient = None
knownServer = (remoteHost, remotePort)
sys.stderr.write('All set.\n')
while True:
    data0, addr0 = s.recvfrom(32768)
    data1 = decrypt("SUPERSECRETPASSWORD", data0)
    addr1 = decrypt("SUPERSECRETPASSWORD", addr0)
    if knownClient is None:
        knownClient = addr1
    if addr1 == knownClient:
        s.sendto(data1, knownServer)
    else:
        s.sendto(data1, knownClient)
