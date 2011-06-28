from __main__ import qt, ctk
import PythonQt

import SlicerVmtk4CommonLib
from StenosisDetectorStep import *

class VisualizationStep(StenosisDetectorStep) :
  """Step implemented using the derivation approach"""
  
  def __init__(self, stepid):
    self.initialize(stepid)
    self.setName( '5. Visualization of detection results' )
    self.setDescription( 'Show the result of stenosis detection' )
    self.__parent=super(VisualizationStep, self)

    
  def createUserInterface(self):
    self.__layout = self.__parent.createUserInterface()
    
    self.__spacerLabel = qt.QLabel(" ")      
    self.__layout.addRow(self.__spacerLabel)
    
    self.__spacerLabel = qt.QLabel("The results look good!")      
    self.__layout.addRow(self.__spacerLabel)
    
    self.__spacerLabel = qt.QLabel("Degree of affectation by stenosis:")      
    self.__layout.addRow(self.__spacerLabel)
    
    self.__affectationGrad = qt.QProgressBar()
    self.__affectationGrad.value = 35
    self.__layout.addRow(self.__affectationGrad)
      
  def validate(self, desiredBranchId):
    self.__parent.validate( desiredBranchId )

