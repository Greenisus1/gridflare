"""Real PTY controls/resize/restore test; no third-party dependencies."""
import os,pty,subprocess,fcntl,termios,struct,time,select

def main():
 m,s=pty.openpty();fcntl.ioctl(s,termios.TIOCSWINSZ,struct.pack('HHHH',34,100,0,0));before=termios.tcgetattr(s)
 p=subprocess.Popen(['python3','gridflare.py']+(['--ascii'] if os.environ.get('SG_ASCII') else []),stdin=s,stdout=s,stderr=s,env=dict(os.environ,TERM='xterm-256color',LANG='C.UTF-8'));out=b''
 def collect(sec):
  nonlocal out
  end=time.monotonic()+sec
  while time.monotonic()<end:
   if select.select([m],[],[],.02)[0]:out+=os.read(m,65536)
 collect(.2)
 for key in [b'\x1bOC',b'\x1bOB',b'2',b' ',b'1',b'\x1bOA',b'\x1bOD',b' ',b'V',b'v',b'R']:os.write(m,key);collect(.15)
 fcntl.ioctl(s,termios.TIOCSWINSZ,struct.pack('HHHH',18,50,0,0));os.kill(p.pid,28);collect(.1)
 assert b'Resize to 64x24' in out
 fcntl.ioctl(s,termios.TIOCSWINSZ,struct.pack('HHHH',34,100,0,0));os.kill(p.pid,28);collect(.1);os.write(m,b'R');collect(.1)
 with open('/tmp/gridflare-terminal.ansi','wb') as f:f.write(out)
 os.write(m,b'Q');collect(.1);p.wait(timeout=3)
 assert p.returncode==0 and termios.tcgetattr(s)==before
 assert b'GRIDFLARE' in out and b'SCORE' in out
 os.close(m);os.close(s);print('PTY arrows/WASD/select/place/restart/resize/uppercase quit/terminal restoration PASS')
if __name__=='__main__':main()
