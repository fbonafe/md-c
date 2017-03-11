import sys
from PyQt4 import QtGui

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 

import random

import numpy as np

from time import sleep

import pymd as pymd



variables = []
variables = ["Temperatura", "E. Potencial", "E. Cinetica", "E. Total"]

running = False

#============================================================================================
#                                        CLASS
#============================================================================================
class RunParam():

    def __init__(self):
        self.npart        = 100
 	self.dt           = 0.0005
	
	self.nsteps       = 1000
	self.totaltime    = 0.0	
	
        self.densPart     = 1.0
	self.cellSize     = 0.0
        
        self.rcut         = 2.5
        self.epsilon      = 0.1
        self.sigma        = 0.2
        self.mass         = 0.3
        self.T0           = 0.4

        self.nproc        = 4
        self.saveevery    = 10

        self.outerloops    = 0
        
#============================================================================================
#                                        CLASS
#============================================================================================
class SolverInterface():
    rpar = RunParam()
    #res  = Results(nvar=2,ndata=1000)        
    def run():
	 
        return 
#=============================================================================================
#                                        CLASS
#============================================================================================
class Results():
    
    def __init__(self):
        self.time = 0
        self.data = 0

    def redim(self,nvar=1, ndata=1):
        self.time = np.zeros(ndata)
        self.data = np.zeros((ndata, nvar))
#============================================================================================
#                                        CLASS
#============================================================================================
class Window(QtGui.QDialog):
    myRunParam = RunParam()
    myResults = Results()
    
    #------------------------------------------------------------------------------------------	
    def __init__(self, parent=None):
        
	self.myRunParam = RunParam()
        self.myResults = Results()

	

        super(Window, self).__init__(parent)
	self.resize(600,600) 	
	
	#w=self.frameGeometry().width() 
	
        self.setWindowTitle('Dinamica Molecular WTPC2017')
	

        # una instancia de figura en la cual dibujar
        self.figure = plt.figure()
	
        # este es el lienzo en el cual se mustra "figure"
        # toma "figure" como un parametro de  __init__
        self.canvas = FigureCanvas(self.figure)
	self.canvas.resize(300,300)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.btnPlot = QtGui.QPushButton('&Ejecutar')
        self.btnPlot.clicked.connect(self.runMD) #plot
	self.btnPlot.setFixedSize(80,20)

	# Boton para carga datos
        self.btnLoadValues = QtGui.QPushButton('&Cargar')
        self.btnLoadValues.clicked.connect(self.loadValues) #plot
	self.btnLoadValues.setFixedSize(80,20)

	#Cuadro de texto nro de particulas
	self.txtNPart = QtGui.QLineEdit()
	self.txtNPart.setFixedSize(60,20)
        self.lblNPart = QtGui.QLabel("Nro de Particulas")	

	#Cuadro de texto tiempo de la simulacion
	self.txtSimTime = QtGui.QLineEdit()
	self.txtSimTime.setFixedSize(60,20)
        self.lblSimTime = QtGui.QLabel("Duracion")
	
	#Cuadro de texto nro de procesadores
	self.txtNProc = QtGui.QLineEdit()
	self.txtNProc.setFixedSize(60,20)
        self.lblNProc = QtGui.QLabel("Nro de Proc.")

	#Cuadro de texto paso de tiempo
	self.txtTStep = QtGui.QLineEdit()
	self.txtTStep.setFixedSize(60,20)
        self.lblTStep = QtGui.QLabel("Paso de tiempo")

        #Cuadro de texto densidad de particulas o cellSize
        ''' Combo box que indica el modo de igresar el nro de particulas ''' 
        self.cmbDensOrCellSize = QtGui.QComboBox(self)
	self.cmbDensOrCellSize.addItem("Densidad de Particulas")
	self.cmbDensOrCellSize.addItem("Tamanio de Celda")
	
	self.txtDensOrCellSize = QtGui.QLineEdit()
	self.txtDensOrCellSize.setFixedSize(60,20)
	
        #Cuadro de texto N steps or total time
        ''' Combo box que indica el modo de igresar la duracion de la simulacion ''' 
        self.cmbNStepsOrTTime = QtGui.QComboBox(self)
	self.cmbNStepsOrTTime.addItem("Nro de pasos")
	self.cmbNStepsOrTTime.addItem("Tiempo Total")

	self.txtNStepsOrTTime = QtGui.QLineEdit()
	self.txtNStepsOrTTime.setFixedSize(60,20)
	
        
        
        #Cuadro de texto radio de corte
	self.txtRcut = QtGui.QLineEdit()
	self.txtRcut.setFixedSize(60,20)
        self.lblRcut = QtGui.QLabel("Radio de Corte")

        #Cuadro de texto Epsilon
	self.txtEpsilon = QtGui.QLineEdit()
	self.txtEpsilon.setFixedSize(60,20)
        self.lblEpsilon = QtGui.QLabel("Epsilon")
	
        #Cuadro de texto Sigma
	self.txtSigma = QtGui.QLineEdit()
	self.txtSigma.setFixedSize(60,20)
        self.lblSigma = QtGui.QLabel("Sigma")
        
        #Cuadro de texto Temperatura inicial
	self.txtT0 = QtGui.QLineEdit()
	self.txtT0.setFixedSize(60,20)
        self.lblT0 = QtGui.QLabel("Temperatura Incial")
	
        

        # Boton para conectar con el metodo que lee los parametros 
        self.btnRun = QtGui.QPushButton('&Leer Datos')
        self.btnRun.clicked.connect(self.readValues)
 	self.btnRun.setFixedSize(80,20)
        
        
  	
        #ComboBox
        self.cmbPostVar = QtGui.QComboBox(self)
        self.cmbPostVar.currentIndexChanged.connect(self.post)
        for text in variables: 
            self.cmbPostVar.addItem(text)
        
        self.lblMonitor = QtGui.QLabel("Monitor")

        #Group box
	SimParamFrame = QtGui.QGroupBox(self)
        SimParamFrame.setTitle("Parametros")

        # set the layout
        layout = QtGui.QHBoxLayout()
        
        #
        gridLayout = QtGui.QGridLayout()
	
        layout.addLayout(gridLayout)		

	
	#Sin Tabs: 
        #layout.addWidget(self.canvas)
	

	#Tab
        self.tabwidget = QtGui.QTabWidget()
        tab1	= QtGui.QWidget()
        tab2	= QtGui.QWidget()
        layoutTab1 = QtGui.QFormLayout()
        layoutTab1.addWidget(self.canvas)
        tab1.setLayout(layoutTab1)
        self.tabwidget.addTab(tab1,"Monitor")
        self.tabwidget.addTab(tab2,"Modelo")

       

        layout.addWidget(self.tabwidget)
        gridLayout.addWidget(self.btnLoadValues,0,0)       
	gridLayout.addWidget(self.lblNPart,1,0)
        gridLayout.addWidget(self.lblTStep,2,0)
	gridLayout.addWidget(self.cmbNStepsOrTTime,3,0)	
	gridLayout.addWidget(self.cmbDensOrCellSize,4,0)


        gridLayout.addWidget(self.lblRcut,5,0) 
        gridLayout.addWidget(self.lblEpsilon,6,0)
        gridLayout.addWidget(self.lblSigma,7,0)
        gridLayout.addWidget(self.lblT0,8,0)

	gridLayout.addWidget(self.lblNProc,9,0)

        gridLayout.addWidget(self.lblMonitor,10,0)
        #.........................................

	gridLayout.addWidget(self.txtNPart,1,1)
	gridLayout.addWidget(self.txtTStep,2,1)

        gridLayout.addWidget(self.txtNStepsOrTTime,3,1)
        gridLayout.addWidget(self.txtDensOrCellSize,4,1)
        
        gridLayout.addWidget(self.txtRcut,5,1)
        gridLayout.addWidget(self.txtEpsilon,6,1)
        gridLayout.addWidget(self.txtSigma,7,1)
        gridLayout.addWidget(self.txtT0,8,1)
        
        gridLayout.addWidget(self.txtNProc,9,1)
        
        gridLayout.addWidget(self.cmbPostVar,10,1)

	gridLayout.addWidget(self.btnRun,11,0)
        gridLayout.addWidget(self.btnPlot,12,0)

	

        self.setLayout(layout)

#------------------------------------------------------------------------------------------
    def loadValues(self):
        self.txtNPart.setText(str(self.myRunParam.npart))
        self.txtTStep.setText(str(self.myRunParam.dt))
	if self.cmbNStepsOrTTime.currentText() == "Nro de pasos":
            self.txtNStepsOrTTime.setText(str(self.myRunParam.nsteps))
        elif self.cmbNStepsOrTTime.currentText() == "Tiempo Total":
            self.txtNStepsOrTTime.setText(str(self.myRunParam.totaltime))
        if self.cmbDensOrCellSize.currentText() == "Densidad de Particulas":
            self.txtDensOrCellSize.setText(str(self.myRunParam.densPart))   
        elif self.cmbDensOrCellSize.currentText() == "Tamanio de Celda":
            self.txtDensOrCellSize.setText(str(self.myRunParam.cellSize))
        self.txtRcut.setText(str(self.myRunParam.rcut))
        self.txtEpsilon.setText(str(self.myRunParam.epsilon))
        self.txtSigma.setText(str(self.myRunParam.sigma))
        self.txtT0.setText(str(self.myRunParam.T0))
        self.txtNProc.setText(str(self.myRunParam.nproc)) 
#------------------------------------------------------------------------------------------  
    def cmbPostVarChangeText(self):
        varIndex = variables.index(self.cmbPostVar.currentText()) 
        return varIndex
#------------------------------------------------------------------------------------------
    def plotResults(self,x,y,n):
        ''' plot y vs x '''
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(x[0:n-1],y[0:n-1],'o-')
 	self.figure.canvas.draw()
        # refresh canvas
        self.canvas.draw()
        self.figure.canvas.flush_events()
#------------------------------------------------------------------------------------------
    def readValues(self):
        ''' Lee los valores de las cuadros de textos para ser pasados como argumento '''
        
        self.myRunParam.npart = int(self.txtNPart.text())
	self.myRunParam.dt    = float(self.txtTStep.text())
	
        #print 'self.cmbNStepsOrTTime.currentText(): ', self.cmbNStepsOrTTime.currentText()
        if self.cmbNStepsOrTTime.currentText() == "Nro de pasos":
            #print 'Se ingresa el nro de pasos...'
            self.myRunParam.nsteps = int(self.txtNStepsOrTTime.text())
            #calculo el tiempo total:
            self.myRunParam.totaltime = float(self.myRunParam.nsteps) * self.myRunParam.dt      
	elif self.cmbNStepsOrTTime.currentText() == "Tiempo Total":
            #print 'Se ingresa el tiempo total...'
            self.myRunParam.totaltime = float(self.txtNStepsOrTTime.text())
            #Calculo el nro de pasos:
            #aca considero que el usuario siempre va a ingresar un tiempo total tal que al dividir en dt se obtendra un nro entero.
            self.myRunParam.nsteps = int(self.myRunParam.totaltime / self.myRunParam.dt) 
        
        #print 'self.cmbDensOrCellSize.currentText(): ', self.cmbDensOrCellSize.currentText()
	if self.cmbDensOrCellSize.currentText() == "Densidad de Particulas":
            #print 'Se ingresa la densidad de particulas...'
            self.myRunParam.densPart = float(self.txtDensOrCellSize.text())
            #calculo el tamanio de la celda:
            #   densidad = nro particulas / cellSize**3  -> cellSize = (nro particulas / densidad) ** 1/3 
            self.myRunParam.cellSize = float(self.myRunParam.npart) / self.myRunParam.densPart
	    self.myRunParam.cellSize = self.myRunParam.cellSize**(1.0/3.0)	     
	elif self.cmbDensOrCellSize.currentText() == "Tamanio de Celda":
            #print 'Se ingresa el tamanio de celdas...'
            self.myRunParam.cellSize = float(self.txtDensOrCellSize.text())
            #Calculo la densidad:
            self.myRunParam.densPart = float(self.myRunParam.npart) / self.myRunParam.cellSize**3
            
	self.myRunParam.Rcut = float(self.txtRcut.text())
	self.myRunParam.Epsilon = float(self.txtEpsilon.text())
        self.myRunParam.Sigma = float(self.txtSigma.text())
        self.myRunParam.T0 = float(self.txtT0.text())
        self.myRunParam.nproc = int(self.txtNProc.text())


        print 'Nro de Particulas        : ',self.myRunParam.npart
        print 'Paso de tiempo           : ',self.myRunParam.dt
 	
        print 'Duracion de la Simulacion: ',self.myRunParam.totaltime  
        print 'Nro de pasos             : ',self.myRunParam.nsteps
        
        print 'Densidad de Particulas   : ',self.myRunParam.densPart  
        print 'Tamanio de Celda         : ',self.myRunParam.cellSize  
        
        print 'Radio de corte           : ',self.myRunParam.rcut  
        print 'Epsilon                  : ',self.myRunParam.epsilon  
        print 'Sigma                    : ',self.myRunParam.sigma
        print 'T0                       : ',self.myRunParam.T0

        print 'Nro de Procesadores      : ',self.myRunParam.nproc
#------------------------------------------------------------------------------------------        
    def post(self):
        '''  '''
        if running == False:
            ivar = self.cmbPostVarChangeText()        
            self.plotResults(self.myResults.time,self.myResults.data[:,ivar],self.myRunParam.outerloops)
#------------------------------------------------------------------------------------------ 
    def runMD(self):
        self.readValues()
        self.myRunParam.outerloops = int(self.myRunParam.nsteps/self.myRunParam.saveevery)
        self.myResults.redim(4,self.myRunParam.outerloops)
	self.btnRun.setEnabled(False) 
        my_system = pymd.System(n_particles=self.myRunParam.npart, 
                                n_steps=self.myRunParam.nsteps, 
                                timestep=self.myRunParam.dt, saveevery=10)
        my_clist  = pymd.CellList()
        my_integ  = pymd.Integrator()
        this_MD   = pymd.MD(my_system, my_clist, my_integ)
        
        

        #["Temperatura", "E. Potencial", "E. Cinetica", "E. Total"]
	running = True
        for i in range(self.myRunParam.outerloops):
            ivar = self.cmbPostVarChangeText()
            self.myResults.time[i] = float(i) * self.myRunParam.dt          
            self.myResults.data[i,1], self.myResults.data[i,2]  = this_MD.runInnerLoop(i)
	    self.myResults.data[i,3] = self.myResults.data[i,1] +  self.myResults.data[i,2]	
            self.plotResults(self.myResults.time[0:i],self.myResults.data[0:i,ivar],i)
        self.btnRun.setEnabled(True)
        running = false  
	return
#============================================================================================
#                                        MAIN
#============================================================================================
def main():
    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())	
    

if __name__ == '__main__':
    main()    
	
    	

    
