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
    ''' Estructura de datos de los parametros de la simulacion.'''
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

        self.outerloops   = 0
        
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
    ''' Estructura de datos de resultados. 
        Se incluyen los nombres de cada resultado y de la variable independiente.
    '''
    def __init__(self):
        self.time = 0
        self.data = 0
        self.ndata = 0
        self.independentParName = "Tiempo"
        self.varName = variables
    def redim(self,nvar=1, ndata=1):
        self.time = np.zeros(ndata, dtype='float64')
        self.data = np.zeros((ndata, nvar), dtype='float64')
#============================================================================================
#                                        CLASS
#============================================================================================
class Window(QtGui.QDialog):
    myRunParam = RunParam()
    myResults = Results()
    
    #------------------------------------------------------------------------------------------	
    def __init__(self, parent=None):
        '''Inicializa el formulario de la interfaz grafica. Posiciona los diferentes componentes (cuadros de texto, liezos, etc.)'''
	self.myRunParam = RunParam()
        self.myResults = Results()

	

        super(Window, self).__init__(parent)
	self.resize(600,600) 	
	
	#w=self.frameGeometry().width() 
	
        self.setWindowTitle('Dinamica Molecular - WTPC2017')
	

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
        self.btnRun = QtGui.QPushButton('&Ejecutar')
        self.btnRun.clicked.connect(self.runMD) #plot
	self.btnRun.setFixedSize(80,20)

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
        
        self.cmbT0 = QtGui.QComboBox(self)
	self.cmbT0.addItem("T0 (Random)")
	self.cmbT0.addItem("T0 (Maxwell-Boltzman)")


        # Boton para conectar con el metodo que guarda los resultados
        self.btnSaveResults = QtGui.QPushButton('&Guardar Resultados')
        self.btnSaveResults.clicked.connect(self.saveResults)
 	self.btnSaveResults.setFixedSize(140,20)
        
        
  	
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
        gridLayout.addWidget(self.cmbT0,8,0)

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
        gridLayout.addWidget(self.btnSaveResults,12,0)

	

        self.setLayout(layout)

#------------------------------------------------------------------------------------------
    def loadValues(self):
        ''' Carga los valores de los parametros del modelo a la intergaz grafica. '''
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
        plt.ylabel(self.cmbPostVar.currentText())
        plt.xlabel('Tiempo')
 	self.figure.canvas.draw()
        # refresh canvas
        self.canvas.draw()
        self.figure.canvas.flush_events()
#------------------------------------------------------------------------------------------
    def saveResults(self):
        ''' Guarda los resultados. '''
        self.writeCSV(fileName="Resultados.csv",res=self.myResults)
        return
#------------------------------------------------------------------------------------------
    def writeCSV(self,fileName,res):
        ''' Escribe la estructura de resultados en un archivo csv. '''
        f=open(fileName, 'w')
        f.write("%s,%s,%s,%s,%s\n" % (res.independentParName , res.varName[0], res.varName[1], res.varName[2], res.varName[3]) )
        for i1 in range(res.ndata):
            f.write("%f,%f,%f,%f,%f\n" % (res.time[i1], res.data[i1,0], res.data[i1,1], res.data[i1,2], res.data[i1,3]))
        f.close()
        return
#------------------------------------------------------------------------------------------
    def enableDisableWidgets(self,enabled=True):
        self.txtNPart.setEnabled(enabled)
	self.txtTStep.setEnabled(enabled)
        self.txtNStepsOrTTime.setEnabled(enabled)
        self.txtDensOrCellSize.setEnabled(enabled)
        self.txtRcut.setEnabled(enabled)
        self.txtEpsilon.setEnabled(enabled)
        self.txtSigma.setEnabled(enabled)
        self.txtT0.setEnabled(enabled)
        self.txtNProc.setEnabled(enabled)
        self.cmbNStepsOrTTime.setEnabled(enabled)
        self.cmbDensOrCellSize.setEnabled(enabled)
        self.cmbT0.setEnabled(enabled)
        self.btnLoadValues.setEnabled(enabled)
        self.btnSaveResults.setEnabled(enabled)
        self.btnRun.setEnabled(enabled) 
        return
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
        ''' Grafica los resultados luego de finalizada la corrida '''
        if running == False and self.myRunParam.outerloops > 0:
            ivar = self.cmbPostVarChangeText()        
            self.plotResults(self.myResults.time,self.myResults.data[:,ivar],self.myRunParam.outerloops) #
#------------------------------------------------------------------------------------------ 
    def runMD(self):
        ''' Comanda la corrida. Crea el sistema, las celdas, el integrador y el modelo. LLama luego al metodo que corre el modelo.
            En cada llamada al metodo que corre el modelo, se adjuntan los resultados a la estructura de datos de resultados. 
        '''
        self.readValues()
        self.myRunParam.outerloops = int(self.myRunParam.nsteps/self.myRunParam.saveevery)
        self.myResults.redim(4,self.myRunParam.outerloops)
	self.myResults.ndata = self.myRunParam.outerloops
        self.enableDisableWidgets(enabled=False) 
        my_system = pymd.System(size=self.myRunParam.cellSize, n_particles=self.myRunParam.npart, 
                                n_steps=self.myRunParam.nsteps, 
                                timestep=self.myRunParam.dt, saveevery=10,
                                rcut=self.myRunParam.rcut , epsilon=self.myRunParam.epsilon, sigma=self.myRunParam.sigma, 
                                T0=self.myRunParam.T0 )
        my_clist  = pymd.CellList()
        my_integ  = pymd.Integrator()
        this_MD   = pymd.MD(my_system, my_clist, my_integ)
        
        #["Temperatura", "E. Potencial", "E. Cinetica", "E. Total"]
	running = True
        for i in range(self.myRunParam.outerloops):
            ivar = self.cmbPostVarChangeText()
            self.myResults.time[i] = float(i*self.myRunParam.saveevery) * self.myRunParam.dt          
            self.myResults.data[i,:] = this_MD.runInnerLoop(i)
            self.plotResults(self.myResults.time[0:i],self.myResults.data[0:i,ivar],i)
        
        running = False
        self.enableDisableWidgets(enabled=True)   
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
	
    	

    
