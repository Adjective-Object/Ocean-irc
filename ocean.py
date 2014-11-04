import socket, sys
import threading
import time

class Plugin(object):
    """ A generic interface for client-server plugins
    """
    name = "plugin-default"
    parameters = []
    version = 0
    cache_updated = 0

    # Initialization

    def generate_init_params(self):
        """ (client side) generates a list of parameters 
            that report the state of the client 
        """
        json.dumps({"version": parameters[version], "cache-updated": parameters[cache-updated]})
        

    def parse_init_params(self, json):
        """ (server side) parses down the list of init
            params from the client and shits out a list
            of the neccisary data to update the state of
            the client to the state of the server
        """
        pass

    def initialize_client(self, json):
        """ (client side) updates the client from 
            parseInitParams to be in sync with the server
        """
        pass


    # Updating (we don't care about these for now)
    # also it's not finished right now

    def update_server(self, json):
        """ update some parameter in the ser
        """

    def update_client(self, json):
        """ (client side) update the client from a change
            in the server.
        """
        pass

class OceanClient():
    plugins = {}
    listeners = {}

    simple_mode = False
    bot_plugins_inited = False

    socket = None
    nickname = 'oceanman'
    realname = 'Actual Cannibal Shia LaBeouf'
    password = ''

    channels = {}
    readbuf = ''

    # for web client
    outbuf = []

    # CODE COPIED FROM OCEANBOT
    def __init__(self):
        loadPlugins(self)
    
    def send_message(self, to, msg):
        self.send('PRIVMSG %s :%s' % (to, msg))

    def send(self, msg):
        self.socket.send(msg + "\r\n")

    def get_sender(self, line):
        return line[0][1:line[0].find('!')]

    def get_recipient(self, line):
        return line[2]

    def register(self, username, realname, nick=None):
        self.username = username
        if nick:
            self.nick=nick

    def bot_init_plugins(self):
        if not self.bot_plugins_inited:
            payload = '{"init": {'
            for plugin in self.plugins:
                payload += '"%s": %s,' % (plugin.name,
                    plugin.generate_init_params)
            payload = payload[:-1]
            payload += '}}'
        print "Sending payload %s" % payload
        self.send_message('ocean-bot', payload)
        self.bot_plugins_inited = True

    def connect(self, host, port=6667):
        self.host = host

        self.socket = socket.socket()
        self.socket.settimeout(None)
        self.socket.connect((host, port))

        if self.nick:
            self.send("NICK %s" % self.nick)
        self.send("USER %s 0 * :%s" % (self.username,self.realname))
        #self.send("JOIN #general")
        self.send("WHOIS ocean-bot")

    def send_command(self, command, args):
        print "sending %s %s" % (command, args)
        if command == 'JOIN':
            self.send('JOIN %s' % args)
        elif command == 'NAMES':
            self.send('NAMES %s' % args)
        else:
            # Blindly sends /COMMAND ARGS as COMMAND ARGS
            self.send('%s %s' % (command, args))

    def read_send_loop(self):
        run_thread = threading.Thread(target=self.run)
        run_thread.daemon = True
        run_thread.start()

        while True:
            line = sys.stdin.readline()
            line = line.strip()
            line = line.split(' ', 1)
            if line[0][0] == '/':
                self.send_command(line[0][1:], line[1])
            else:
                self.send_message(line[0], line[1])
            print self.read_outbuf()
            self.clear_outbuf()

    def read_outbuf(self):
        return self.outbuf

    def clear_outbuf(self):
        self.outbuf = []

    def get_channels(self):
        return self.channels

    def run(self):

        while True:
            self.readbuf += self.socket.recv(1024).decode('UTF-8')
            lines = self.readbuf.split('\n')
            self.readbuf = lines.pop()
            for line in lines:
                print line
                line = line.split(' ')

                if line[0] == 'PING':
                    self.send('PONG %s\r\n' % line[1])       

                elif line[1] == 'PRIVMSG':
                    # cli_print(line) #FOR DEBUG/CLI
                    # Channel Messages
                    if '#' in line[2]:
                        self.outbuf.append({
                            u'channel': self.get_recipient(line),
                            u'usr':  self.get_sender(line),
                            u'msg': ' '.join(line[3:]).strip()[1:],
                            u'timestamp': str(time.time()).encode('UTF-8')
                        })
                    # Private Messages
                    if line[2] == self.nickname:
                        self.outbuf.append({
                            u'channel': self.get_sender(line),
                            u'usr':  self.get_sender(line),
                            u'msg': ' '.join(line[3:]).strip()[1:],
                            u'timestamp': str(time.time()).encode('UTF-8')
                        })

                # Numeric Messages
                elif line[1].isdigit():
                    if line[1] == '401' and line[3] == 'ocean-bot':
                        self.simple_mode = True
                    elif line[1] == '311' and line[3] == 'ocean-bot':
                        self.bot_init_plugins()
                    elif line[1] == '332':
                        if not line[3] in self.channels:
                            self.channels[line[3]] = {}
                        # Public doesn't belong here!!
                        self.channels[line[3]]['public'] = True
                        self.channels[line[3]]['topic'] = ' '.join(line[4:])
                    elif line[1] == '353':
                        if not line[4] in self.channels:
                            self.channels[line[4]] = {}
                        self.channels[line[4]]['users'] = [
                            {'nick': nick.replace(':', '').strip(),
                                'realname': 'Shia LaBeouf'}
                            for nick in line[5:]]
                    else:
                        #print ' '.join(line)
                        pass
                else:
                    #print ' '.join(line)
                    pass

def cli_print(line):
    sender = line[0][1:line[0].find('!')]
    print "[%s] %s%s" % (line[2], sender, ' '.join(line[3:]))

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
    if len(sys.argv) > 1 and sys.argv[1] == 'bot':
        bot = OceanBot()
        while True:
           bot.run()
    else:
        cli = OceanClient()
        cli.register("oceanman", "Max HH", nick="oceanman")
        cli.connect("104.236.63.94")
        cli.read_send_loop()
