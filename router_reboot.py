import telnetlib, getpass

#take arugments also
host = '192.168.6.1'
user = 'admin'
password = 'yourpassword'
port = 23
timeout = 5

if host:
    #start with reboot function
    session = telnetlib.Telnet(host, port, timeout)
    session.open(host, port, timeout)
#     logger.debug('verify_emails: Connected to HOST: {0} on PORT: {1}.'.format(mxrecord, port))
    check = session.expect([b"name:"])
    check = session.write(b"admin" + b"\r")
    print(check)
    exit()
    check = session.read_until(b"name:")
    print(check)
    session.write(b"admin" + b"\r")
    check = session.read_until(b"\r")
    # check = session.expect([b"\\n"])
    print(check)
    exit()

