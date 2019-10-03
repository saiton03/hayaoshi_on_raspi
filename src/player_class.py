import time
import RPi.GPIO as GPIO
from multiprocessing import Value, Array, Process, Lock

class player:
  def __init__(self,inpin,outpin):
    self.inpin=inpin  # input pin no.
    self.outpin=outpin  # output pin no.
    self.pressed = False  # Is switch pressed
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.inpin,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)  # 電圧がhighのとき，high
    GPIO.setup(self.outpin,GPIO.OUT)
    GPIO.output(self.outpin,False)

  def led_state(self):
    return GPIO.input(self.outpin)

  def led_high(self):
    GPIO.output(self.outpin,True)

  def led_low(self):
    GPIO.output(self.outpin,False)

  def led_change(self):  # 指定がなければon off切り替え
    GPIO.output(self.outpin,not GPIO.input(self.outpin))

  def switch_state(self):
    return GPIO.input(self.inpin)
  
  def proc(self, lock, i, itr, cnt, que, press):
    while True:
      self.led_low()
      if not press[i]:
        if self.switch_state():
          press[i] = 1
          lock.acquire()
          st=''
          try:
            que[cnt.value] = i
            cnt.value += 1
            # print('player {} pressed!:{}'.format(i,que[itr.value:cnt.value]))
            st = 'player {} pressed!:{}'.format(i,que[itr.value:cnt.value])
          finally:
            lock.release()
            print(st)
      while que[itr.value] == i:
        self.led_change()
        time.sleep(0.3)

  


