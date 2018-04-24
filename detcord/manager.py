'''
Keep track of all credentials and connections per host
'''

from .exceptions import *
import paramiko

class Manager(object):
    def __init__(self):
        self.manager = {}
        self.default_pass = "changeme"
        self.default_user = "root"
        self.timeout = 2

    def addHost(self, host, port=22, user=None, password=None):
        if not user:
            user = self.default_user
        if not password:
            password = self.default_pass
        self.manager[host.lower()] = {
            'port': port,
            'user': user,
            'pass': password
        }

    def getSSHConnection(self, host):
        '''Get the connection for that host or create a
        new connection if none exists
        '''
        host = host.lower()
        if host not in self.manager:
            raise HostNotFound("{} not in Manager".format(host))
        con = self.manager[host].get('ssh', None)
        if con is None:
            self.manager[host]['ssh'] = self.connect(host)
        return con

    def connect(self, host):
        port = self.manager[host]['port']
        user = self.manager[host]['user']
        passwd = self.manager[host]['pass']
        con = paramiko.SSHClient()
        con.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
        con.load_system_host_keys()
        con.connect(timeout=self.timeout, hostname=host, port=port, username=user, password=passwd)
        return con
