import fcntl
import termios
import sys
import os

def getkey():
  fno=sys.stdin.fileno()

  attr_old=termios.tcgetattr(fno)

  attr=termios.tcgetattr(fno)
  # print(attr[3])
  attr[3] & ~termios.ECHO & ~ termios.ICANON
  termios.tcsetattr(fno,termios.TCSADRAIN,attr)

  fcntl_old=fcntl.fcntl(fno,fcntl.F_GETFL)
  fcntl.fcntl(fno, fcntl.F_SETFL, fcntl_old | os.O_NONBLOCK)
  try:
    rd=sys.stdin.read(1)
  finally:
    fcntl.fcntl(fno,fcntl.F_SETFL,fcntl_old)
    termios.tcsetattr(fno,termios.TCSANOW,attr_old)
  return rd
