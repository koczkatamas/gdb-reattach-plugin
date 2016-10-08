from __future__ import with_statement
import psutil
import subprocess
import time
import gdb

def pidof(pgname):
    pids = []
    for proc in psutil.process_iter():
        # search for matches in the process name and cmdline
        try:
            name = proc.name()
        except psutil.Error:
            pass
        else:
            if pgname in name:
                pids.append(proc.pid)
                continue

        try:
            cmdline = proc.cmdline()
        except psutil.Error:
            pass
        else:
            if cmdline and pgname in cmdline[0]:
                pids.append(proc.pid)

    return pids

class WaitforCommand (gdb.Command):
    def __init__ (self):
        self.lastFn = ''
        super (WaitforCommand, self).__init__ ("waitfor", gdb.COMMAND_SUPPORT, gdb.COMPLETE_FILENAME)

    def invoke (self, arg, from_tty):
        args = arg.split(' ')
        
        fn = [arg for arg in args if not arg.startswith('-')] [-1]
        if len(fn) > 0:        
            self.lastFn = fn
        
        if len(self.lastFn) == 0:
            print('You have to specify the name of the process (for pidof) for the first time (it will be cached for later)')
            return
            
        while True:
            try:
                pids = pidof(self.lastFn)
                if len(pids) > 0:
                    break
                #pid = subprocess.check_output(["pidof", self.lastFn], bufsize=1024, stdout=subprocess.PIPE, stderr=subprocess.PIPE).strip()
            except subprocess.CalledProcessError as e:
                if e.returncode != 1:
                    raise e
            time.sleep(0.1)
            
        print('PID: %r' % pids)
        
        gdb.execute('attach ' + str(pids[0]))
        if '-c' in args:
            gdb.execute('c')

WaitforCommand()