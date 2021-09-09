# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.lines as mlines

class Simulation:
    """Class that simulates an epidemic.
       It is possible to specify the number of people in the simulation (a grid m by n) and the number of contact
       every person has with one another (r and K) and the probability of being infected and recovered"""
    def __init__(self, m = 40, n = 25, r = 6, k = 20, alpha_infected = 0.01, alpha_recovered = 0):
      """Initialise the simulation and set the parameters"""
      print("The class will be initialised in 5-6 minutes") 
      self.r = r
      self.k = k
      self.n = n
      self.m = m
      self.alpha_infected = alpha_infected
      self.alpha_recovered = alpha_recovered
      self.points = []      
      self.lines = []
      self.pandemic = pd.DataFrame()
      self.connect = []
      self.infected = []     
      count = 0
      while count <= ((m*n*k)/2):
          #it creates points
          x = np.random.choice(a=n, replace=False)
          y = np.random.choice(a=m, replace=False)
          x1 = np.random.choice(a=n, replace=False)
          y1 = np.random.choice(a=m, replace=False)
          #checks that there are not repetitions and plot the points. For each points initialise the status.
          if x1 != x or  y1 != y:
              plt.plot(x, y, marker = ".", color = "gold",  markersize = 1)
              self.points.append([(x, y), np.random.choice(["I", "R", "S"], 1, True, [alpha_infected, alpha_recovered, 1-alpha_infected-alpha_recovered])[0]])
              #Connects points that are distant from one another less than r. It plots the connections. Augment count for the while loop.
              if  np.sqrt((x-x1)**2 + (y-y1)**2) < r: 
                  connections = (x, y), (x1, y1)
                  self.lines.append(connections)
                  count = count + 1
                  plt.plot((x, x1), (y, y1), linestyle = "-", color = "grey")      
    def run(self, gamma = 0.075, beta_recover = 0.05, beta_death = 0.005):
       """It runs the simulation for 100 days. 
          It changes the intial statuses of people that have contact with other people based on the probability of 
          remaining infected, recovering from infection or die."""
       print("The simulation takes 5-6 minutes to run") 
       self.points = pd.DataFrame(self.points)
       self.points.columns = ['xy', 'status']
       self.lines = pd.DataFrame(self.lines)
       self.lines.columns = ['xy', 'x1y1']
       self.gamma = gamma
       self.beta_recover = beta_recover
       self.beta_death = beta_death
       self.status2 = [] 
       self.final_status = []
       #a dataframe with all the points not isolated is needed for the plot implemented in the method plot_state.
       self.connect = self.points[(self.points['xy'].isin(self.lines['xy']) | self.points['xy'].isin(self.lines['x1y1']))]
       self.iterator = 0
       self.day = 100
       #It changes the intial status of susceptible people into infected or leaves them as susceptible based on the
       #probability gamma.
       for i in self.connect['status']:
           if i == 'S':
               self.status2.append(np.random.choice(["I", "S"], 1, True, [self.gamma, 1-self.gamma])[0])
           else:
               self.status2.append(i)
       #changes the status of infected peolple into recovered and dead or leaves them as infected based on the probabilities
       #beta_recovered, beta_death.
       for w in self.status2:
           if w == 'I':
               self.final_status.append(np.random.choice(["R", "D", "I"], 1, True, [self.beta_recover, self.beta_death, 1-self.beta_recover-self.beta_death])[0])
           else:
               self.final_status.append(w)        
       #it repeats the two loops above for 100 days, in this way the status of people can evolve. It adds columns to
       #the dataframe pandemic. Each column is the final status at each day.
       for d in range(1, self.day+1):       
           self.status2 = self.final_status
           for i, u in enumerate(self.status2):
               if u == 'S':
                   self.status2[i] = np.random.choice(["I", "S"], 1, True, [self.gamma, 1-self.gamma])[0]
               else:
                   self.status2[i] = u        
           for i, w in enumerate(self.status2):
               if w == 'I':
                   self.final_status[i] = np.random.choice(["R", "D", "I"], 1, True, [self.beta_recover, self.beta_death, 1-self.beta_recover-self.beta_death])[0]
               else:
                   self.final_status[i] = w
           self.iterator = self.iterator +1
           col_name = 'final_status' + str(self.iterator)
           self.pandemic.loc[:, col_name] = self.final_status
    def plot_state(self, time):
       """It plots the state for each person an any day specified by the user from 1 to 100.""" 
       self.time = time
       #it gets coordinates of all points
       x_val = []
       y_val = []
       for i in self.points['xy']:
           x_val.append(i[0])
           y_val.append(i[1])    
       #it gets initial and final coordinates of lines
       line_x = []
       line_y = []
       for i in self.lines['xy']:
           line_x.append(i[0])
           line_y.append(i[1])    
       line_x1 = []
       line_y1 = []
       for i in self.lines['x1y1']:
           line_x1.append(i[0])
           line_y1.append(i[1])    
       #it gets coordinates of points not isolated
       x_up = []
       y_up = []
       for i in self.connect['xy']:
           x_up.append(i[0])
           y_up.append(i[1])
       #it creates the plot
       fig, ax = plt.subplots(figsize=(20, 15))
       ax.axis('off')
       #for the day specified by the user, it creates a map of different colours for each status.
       colours = self.pandemic['final_status'+str(self.time)].map({'I':'red', 'S':'gold', 'R':'blue', 'D':'black'})
       #it plots points and lines. It leaves as gold the points isolated. It changes the colours for the other points.
       ax.plot((line_x, line_x1), (line_y, line_y1),  linestyle = "-", color = "grey")
       ax.scatter(x_val, y_val,  marker = "o", color = "gold")
       ax.scatter(x_up, y_up,  marker = "o", color=colours)
       blue = mlines.Line2D([], [], color='blue', marker='o', linestyle='None',
                          markersize=6, label='Recovered')
       red = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=6, label='Infected')
       gold = mlines.Line2D([], [], color='gold', marker='o', linestyle='None',
                          markersize=6, label='Susceptible')
       black = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                          markersize=6, label='Dead')
       plt.legend(handles=[blue, red, gold, black], bbox_to_anchor=(1,0.6), title='Day '+str(self.time), fontsize=18,)
    def chart(self):
       """It plots the evolution of the pandemic from day 1 to day 100 in terms of numbers of susceptible, 
          infected, recovered and dead"""
       #it counts how many susceptible, infected, recovered and dead there are every day and 
       #plot them from day 1 to day 100.
       #there are some problems with the number of peolple generated probably due to replications. 
       #The code should be further analysed and changed but for time reason is no possible.
       susceptible = self.pandemic[self.pandemic == 'S'].count()
       self.infected = self.pandemic[self.pandemic == 'I'].count()
       recovered = self.pandemic[self.pandemic == 'R'].count()
       dead = self.pandemic[self.pandemic == 'D'].count()
       plt.plot(range(0, 100), susceptible, linestyle = '-', color = 'gold')
       plt.plot(range(0, 100), self.infected, linestyle = '-', color = 'red')
       plt.plot(range(0, 100), recovered, linestyle = '-', color = 'blue')
       plt.plot(range(0, 100), dead, linestyle = '-', color = 'black')
       plt.xlabel('Time')
       plt.ylabel('Number')
       #it adds a legend.
       blue = mlines.Line2D([], [], color='blue', linestyle='-', label='Recovered')
       red = mlines.Line2D([], [], color='red', linestyle='-', label='Infected')
       gold = mlines.Line2D([], [], color='gold', linestyle='-', label='Susceptible')
       black = mlines.Line2D([], [], color='black', linestyle='-', label='Dead')
       plt.legend(handles=[blue, red, gold, black], bbox_to_anchor=(1.35,0.7), title='', fontsize=10,)
    def max_infected(self):
       """It returns the maximum number of infected individuals""" 
       self.max_infected = max(self.infected)
       return('Maximum number of infected people is {}'.format(self.max_infected))
    def peak_infected(self):
       """It returns the day at which the number of infected individuals was maximal""" 
       self.peak_infected = self.infected.reset_index()
       self.peak_infected.columns = ['final_statuses', 'number']
       return('The maximum number of infected people is after {} days'.format(self.peak_infected.number.idxmax()))
    @classmethod
    def averaged_chart(cls, N=100, m = 40, n = 25, r = 6, k = 20, alpha_infected = 0.01, alpha_recovered = 0):
       """Class method that runs the simulation N times. It should return an averaged plot of the pandemic evolution
          and averaged max_infected and pea_infected for each run."""         
       for i in range(0, N):
           i = Simulation()
           i.chart()
           i.max_infected
           i.peak_infected
       







s = Simulation(m = 20, n = 12, r = 2, k = 4)
s.run()
s.plot_state(2)
s.chart()
s.max_infected()
s.peak_infected()


Simulation.averaged_chart(N=2, m=10, n=5, r=2, k=4)



