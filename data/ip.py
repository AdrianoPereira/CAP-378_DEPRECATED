import threading
import time


class execute(threading.Thread):
   def __init__ (self, n):
      threading.Thread.__init__(self)
      self.n = n
      
   def run(self):
      print('Starting thread %d...'%self.n)
      print('executing Thread %d'%self.n)
      time.sleep(2)
      print('finishied thread %d'%self.n)
      
def run(n):
    print('Starting thread %d...'%n)
    print('executing Thread %d'%n)
    time.sleep(2)
    print('finishied thread %d'%n)


for x in range(20):
    run(x+1)
    