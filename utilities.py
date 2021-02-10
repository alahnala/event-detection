from termcolor import colored
import datetime, time

def cprint(msg, logname="log", error=False, important=False, p2c=True):
    tmsg = msg if not important else colored(msg, 'cyan')
    tmsg = tmsg if not error else colored(msg, 'red')
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    cmsg = str(st) + ': ' + str(tmsg)
    tmsg = str(st) + ': ' + str(msg)
    if p2c:
        print(cmsg)
    log_file = open('logs/' + logname + '.log', 'a')
    log_file.write(tmsg + '\n')
    log_file.close()