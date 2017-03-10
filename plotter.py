""" 
.. module:: plotter
    :platform: GNU Linux
    :synopsis: This module contains a Class names Plotter that plots the outputs of the program, like energy vs time, in real time.
.. moduleauthor:: TeaMD #WTPC17

"""
import matplotlib.pyplot as plt
class Plotter (object):
    """
    This class creates a plot. It defines title, axis labels and type of scatter.
    
    :attr size: number of particles per side of the box
    :attr color: color of the scatter point
    :attr marker: type of scatter point
    :attr x_label: label of x axis
    :attr y_label: label of y axis
    :attr fig,ax: tells about the status of fig and ax

    """
    def __init__(self, x_label, y_label) :
        self.size = 1000
        self.color = 'red'
        self.marker = 'o'
        self.x_label = x_label
        self.y_label = y_label
        self.fig = None
        self.ax = None
    
    def plot1(self, x, y):
        """
        Method of class Plotter.
        
        :param x: first variable to plot 
        :param y: second variable to plot
        :type x: double - array
        :type y: double - array
        
        """
        if self.fig == None:
            plt.ion() 
            self.fig, self.ax = plt.subplots()
        
        total_time = 100 #n_steps*dt
        self.ax.set_xlim((0, total_time))
        self.ax.set_ylim((1,100))
        self.ax.set_title('%s vs %s'%(self.y_label,self.x_label))
        self.ax.scatter(x,y,self.size,self.color,self.marker)
        plt.show()
        plt.pause(0.0001)

    