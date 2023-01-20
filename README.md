# loading_screen_pygame
Simulate a loading screen in pygame.

## Some notes:
* Use deque or Queue
  * Qeueu allows waiting if queue is full
  * deque is faster
* Use daemon threads
  * Quits when main thread quits
* Load data into a generator then use iter
  * Use the least amount of memory

