import sys, socket
from simplecrypt import encrypt, decrypt
from Tkinter import *


def out(reason):
    sys.stderr.write(reason + '\n')


def fail(reason):
    sys.stderr.write("FAILURE: " + reason + '\n')
    sys.exit(0)


localPort = ""
remoteHost = ""
remotePort = ""

On = False
Error=False


def test(localPort, remoteHost, remotePort):
    if sys.argv.__len__() == "1":
        localPort, remoteHost, remotePort = sys.argv[1].split(':')
    if localPort == "":
        out("localport IS INVALID(Only normal for startup)")
        Error=True
    if remoteHost == "":
        out("remotehostt IS INVALID(Only normal for startup)")
        Error = True
    if remotePort == "":
        out("remoteport IS INVALID(Only normal for startup)")
        Error = True



def start(Error, On):
    test(localPort, remoteHost, remotePort)
    if Error != False:
        On = True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', localPort))
    except:
        out('Failed to bind on port(Only normal for startup) ' + str(localPort))

    knownClient = None
    knownServer = (remoteHost, remotePort)
    sys.stderr.write('All set.\n')
    while On:
        data0, addr0 = s.recvfrom(32768)
        data1 = encrypt("SUPERSECRETPASSWORD", data0)
        addr1 = encrypt("SUPERSECRETPASSWORD", addr0)
        if knownClient is None:
            knownClient = addr1
        if addr1 == knownClient:
            s.sendto(data1, knownServer)
        else:
            s.sendto(data1, knownClient)


if len(sys.argv) != 2 or len(sys.argv[1].split(':')) != 3:
    out('Usage: udp-relay.py localPort:remoteHost:remotePort')
    out("Depending on GUI.")
else:
    start(Error, On)


# GUI STUFF DOWN HERE
def pack():
    LPF.pack()
    localPortField.pack()
    RHF.pack()
    remoteHostField.pack()
    RPF.pack()
    remotePortField.pack()
    Start.pack()


Start = Button(height="1", text="Start", width="40", command=start(Error, On))
LPF = Label(height="1", text="localPort", width="9")
RHF = Label(height="1", text="remoteHost", width="10")
RPF = Label(height="1", text="remotePort", width="10")
localPortField = Text(height="1", width="5")
remoteHostField = Text(height="1", width="16")
remotePortField = Text(height="1", width="5")

if localPortField.get("1.0", 'end-1c') != localPort:
    localPort = localPortField.get("1.0", 'end-1c')
if remoteHostField.get("1.0", 'end-1c') != remoteHost:
    remoteHost = remoteHostField.get("1.0", 'end-1c')
if remotePortField.get("1.0", 'end-1c') != remotePort:
    remotePort = remotePortField.get("1.0", 'end-1c')

pack()
mainloop()
