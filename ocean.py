import socket, sys


class Plugin(object):
    """ A generic interface for client-server plugins
    """
    name = "plugin-default"
    parameters = []


    # Initialization

    def generateInitParams(self):
        """ (client side) generates a list of parameters 
            that report the state of the client 
        """
        pass

    def parseInitParams(self, json):
        """ (server side) parses down the list of init
            params from the client and shits out a list
            of the neccisary data to update the state of
            the client to the state of the server
        """
        pass

    def initializeClient(self, json):
        """ (client side) updates the client from 
            parseInitParams to be in sync with the server
        """
        pass


    # Updating (we don't care about these for now)
    # also it's not finished right now

    def updateServer(self, json):
        """ update some parameter in the ser
        """

    def updateClient(self, json):
        """ (client side) update the client from a change
            in the server.
        """
        pass




class OceanClient():

    nickname = ''
    password = ''

    plugins = {}
    listeners = {}

    realname = "Anon"
    nick = None

    def __init__(self):
        loadPlugins(self)
        self.buffer = ""
        
    def readline(self):
        instr = self.socket.recv(4096)
        self.buffer += instr
        spl = self.buffer.split("\n", 1)

        if len(spl) == 2:
            self.buffer = spl[1]
            return spl[0]
        else:
            #print "buffer:", self.buffer
            sys.stdout.flush()
            #return self.readline()

    def send(self, msg):
        self.socket.send(msg + "\r\n")

    def register(self, username, realname, nick=None):
        self.username = username
        if nick:
            self.nick=nick

    def flushTo(self, start):
        line=self.readline()
        while (not line.startswith(start)):
            print "...", line
            if(line.startswith("PING")):
                print "PING"
                self.pong(line)
            line=self.readline()
        self.buffer = line + self.buffer

    def flushToNumeric(self, numcode):
        self.flushTo(":")
        s = self.readline()
        while not self.checkNumeric(s, numcode):
            self.flushTo(":")
            s = self.readline()
            print ">..."

        self.buffer = s + self.buffer

    def checkNumeric(self, line, num):
        spl = line.split(" ")
        return spl[0].startswith(":") and int(spl[1]) == num 

    def pong(self, pingstr):
        spl = pingstr.split(" ")
        msg = "PONG"
        for i in spl[1:]:
            msg+=" "+i
        self.send(msg)

    def connect(self, host, port=6667):
        self.host = host

        self.socket = socket.socket()
        self.socket.settimeout(None)
        self.socket.connect((host, port))

        if self.nick:
            self.send("NICK %s"%self.nick)
        self.send("USER %s 0 * :%s"%(self.username,self.realname))

        self.send("JOIN #general")
        self.send("")
        self.send("WHOIS ocean-bot")

        self.flushToNumeric(311)
        while(True):
            self.readline()



def loadPlugins(oceanCli):
    #oceanCli.plugins
    pass

class OceanBot(object):
    socket = None
    nickname = 'ocean-bot'
    # CHANGE THIS
    channels = ['#general']
    readbuf = ''

    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('104.236.63.94', 6667))
        self.send('NICK %s' % self.nickname)
        self.send('USER %s %s * :%s' % ('ocean-bot', '0', self.nickname))
        self.send('JOIN %s' % self.channels[0])
    
    def get_sender(self, line):
        return line[0][1:line[0].find('!')]

    def get_recipient(self, line):
        return line[2]

    def send_message(self, to, msg):
        self.send('PRIVMSG %s :%s' % (to, msg))

    def send(self, msg):
        self.socket.send(msg + '\r\n')

    def run(self):
        self.readbuf = self.readbuf + self.socket.recv(1024).decode('UTF-8')
        lines = self.readbuf.split('\n')
        self.readbuf = lines.pop()

        for line in lines:
            print line
            line = line.rstrip()
            # Only spaces characters constitute whitespace
            line = line.split(' ')


            if line[0] == 'PING':
                self.send('PONG %s\r\n' % line[1])       

            # Channel/Private Messages
            if line[1] == 'PRIVMSG':
                if '#' in line[2]:
                    self.send_message(self.get_recipient(line), 'YOU SAID A THING')
                if line[2] == self.nickname:
                    self.send_message(self.get_sender(line), 'hello yes i am ocean bot good day')

if __name__ == "__main__":
    #cli = OceanClient()
    #cli.register("oceanman", "Max HH", nick="oceanman")
    #cli.connect("104.236.63.94")
    bot = OceanBot()
    while True:
        bot.run()
