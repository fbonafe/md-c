import matplotlib.pyplot as plt
class Plotter (object):
    def __init__(self, x_label, y_label) :
        self.size = 1000
        self.color = 'red'
        self.marker = 'o'
        self.x_label = x_label
        self.y_label = y_label
        self.fig = None
        self.ax = None
    
    def plot1(self, x, y):
        
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

    