from queue import Queue
q=Queue()
for i in range(5):
    q.put(i)
    
j=q.get()
print(j)