#!/usr/bin/python3

import threading
import time

exitFlag = 0

class sensorExecutor(threading.Thread):

   def __init__(self, threadID, name, delay):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.delay = delay

   def run(self):
      print ("Starting " + self.name)
      print_time(self.name, self.delay, 20)
      print ("Exiting " + self.name)

def print_time(threadName, delay, counter):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s. %s" % (threadName, time.time(), counter))
      counter -= 1

if __name__ == "__main__":

      # Create data structure

      # Execute threads

      # Verify data is present
      

      # Create new threads
      thread1 = sensorExecutor(1, "Thread-1", 0.01)
      thread2 = sensorExecutor(2, "Thread-2", 0.01)

      # Start new Threads
      thread1.start()
      thread2.start()
      thread1.join()
      thread2.join()
      print ("Exiting Main Thread")