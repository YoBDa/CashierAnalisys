from collections import deque
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

class Client(object): # A class representing client
    ticks_waited = 0

class Cashier(object): # A class representing cashier
    state = False  # False - free, True - busy
    ticks = 0

    def tick(self):
        if self.state:
            self.ticks += 1

        if self.ticks > 2:
            self.ticks = 0
            self.state = False
            return 1
        return 0


q = deque()  # the queue for cashier
processed_clients = [] # array storing processed clients
ticks = 500  # time limit
cashier = Cashier()


counter = 0 
client_counter = 0
processed_counter = 0
max_queue_length = 0
average_queue_length = 0
average_waiting_time = 0

cashier_states = [] # array storing cashier state on every tick
queue_lengths = [] # array storing queue length on every tick
processed_tickets = [] # array storing number of processed clients every tick

for i in range(ticks):
    input_thread = random.randint(0, 1)  # Input thread generator
    if input_thread == 1: # client counter
        client_counter += 1


    counter += 1  # tick counter
    qlength = len(q) # queue length

    if input_thread == 1 and not cashier.state:  # if input 1 & cashier is free
        cashier.state = True  # let cashier busy


    elif input_thread == 1 and cashier.state:  # if input 1 & cashier is busy
        q.append(Client())  # append queue


    elif input_thread == 0 and not cashier.state:  # if input 0 & cashier is free
        if qlength > 0:  # if queue length > 0
            cashier.state = True  # let cashier busy from queue
            processed_clients.append(q.popleft())

    for client in q:
        client.ticks_waited += 1

    if max_queue_length < qlength:
        max_queue_length = qlength

    processed_counter += cashier.tick()  # tick cashier
    processed_tickets.append(processed_counter)  # save count of processed tickets
    queue_lengths.append(qlength) # save queue lengths
    cashier_states.append(int(cashier.state)) # save cashier states


# Basic analisys

df = pd.DataFrame({
    'qlength': queue_lengths,
    'cstate': cashier_states,
    'proctickets': processed_tickets
})

processed_clients.extend(q)

average_waiting_time = np.mean([client.ticks_waited for client in processed_clients])
average_queue_length = np.mean(queue_lengths)
print('Whole time used: ', ticks)
print('Average waiting time: ', average_waiting_time)
print('Average queue length: ', average_queue_length)
print('Max queue length: ', max_queue_length)
print('Count of processed clients: ', processed_counter)
print('Count of all clients: ', client_counter)


ax = sns.lineplot(data=df, x=df.index, y='qlength')
ax.set(xlabel='time', ylabel='Queue length')

fig = ax.get_figure()
fig.savefig('plot.png')
