import RPi.GPIO as GPIO
import time
import sys
from multiprocessing import Value, Array, Process, Lock
import multiprocessing as mp

import key_event
import player_class


def reset(players, lock, cnt, itr, que,press):
    lock.acquire()
    try:
      for i in range(len(players)+2):
        que[i] = -1
        press[i] = 0
      itr.value = 0
      cnt.value = 0
    finally:
      lock.release()
    print('-----------')

print("start")

mp.set_start_method('fork')

GPIO.setmode(GPIO.BOARD)

# ここを直そう
N=2  # 子機の数
inpin = [12, 16]  # スイッチ側のピン番号
outpin = [11, 15]  # LED側のピン番号

if N!=len(inpin) or N!=len(outpin):
  print("wrong input")
  sys.exit(1)

players =[]
for i,o in zip(inpin,outpin):
  players.append(player_class.player(i,o))

lock=Lock()
loop=True
push=False
cnt = Value('i',0)
itr = Value('i',0)
que = Array('i',N+2)
press = Array('i',N+2)

for j in range(N+2):
  que[j] = -1
process = []
for j in range(N):
  process.append(Process(target=players[j].proc, args=[lock,j, itr, cnt, que,press]))

for p in process:
  p.start()

while loop:
  st=key_event.getkey()
  if st!='':
    if st=='o':
      if cnt.value>itr.value:
        print('player {} correct answer'.format(que[itr.value]))
        reset(players,lock,cnt,itr,que,press)
      else:
        print('Noone has the right to answer')
    elif st=='x':
      if cnt.value>itr.value:
        print('player {} miss: {}'.format(que[itr.value],que[itr.value+1:cnt.value]))
        itr.value += 1
      else:
        print('Noone has the right to answer')
    elif st=='r':
      print('reset')
      reset(players,lock,cnt,itr,que,press)
    elif st=='e':
      loop = False

  time.sleep(0.001)

print('finish')
for p in process:
  p.terminate()
GPIO.cleanup()

