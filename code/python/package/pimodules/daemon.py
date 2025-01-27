import sys
import os
import time
import atexit
import logging
import logging.handlers
from signal import SIGTERM

class Daemon:
    """
    A forking daemon
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        formatter = logging.Formatter('%(module)s[%(process)s]: <%(levelname)s>: %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

        self.pidfile = pidfile
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError as e: 
            sys.stderr.write(f"fork #1 failed: {e.errno} ({e.strerror})\n")
            sys.exit(1)
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError as e: 
            sys.stderr.write(f"fork #2 failed: {e.errno} ({e.strerror})\n")
            sys.exit(1) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+', 0)

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.deletePidFile)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write(f"{pid}\n")
    
    def deletePidFile(self):
        os.remove(self.pidfile)

    def start(self, daemonize=True):
        """
        Start the daemon
        """

        self.daemon = daemonize

        if daemonize:
            # Check for a pidfile to see if the daemon is already running
            try:
                with open(self.pidfile, 'r') as pf:
                    pid = int(pf.read().strip())
            except IOError:
                pid = None
    
        if daemonize:
            if pid:
                message = f"pidfile {self.pidfile} already exist. Daemon already running?\n"
                sys.stderr.write(message)
                sys.exit(1)
        
        # Start the daemon
        if daemonize:
            self.daemonize()

        self.run()

    def stop(self):
        """
        Stop the daemon
        """

        if self.daemon:
            # Get the pid from the pidfile
            try:
                with open(self.pidfile, 'r') as pf:
                    pid = int(pf.read().strip())
            except IOError:
                print('could not get pid')
                pid = None
    
        if self.daemon:
            if not pid:
                message = f"pidfile {self.pidfile} does not exist. Daemon not running?\n"
                sys.stderr.write(message)
                return  # not an error in a restart

        if self.daemon:
            # Try killing the daemon process	
            try:
                while 1:
                    os.kill(pid, SIGTERM)
                    time.sleep(0.1)
            except OSError as err:
                err = str(err)
                if err.find("No such process") > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    print(err)
                    sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        raise NotImplementedError
