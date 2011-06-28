from __main__ import qt, ctk
import PythonQt

import SlicerVmtk4CommonLib
from StenosisDetectorStep import *

class OptimizationStep(StenosisDetectorStep) :
  """Step implemented using the derivation approach"""
  
  def __init__(self, stepid):
    self.__parent=super(OptimizationStep, self)
    self.__parent.__init__(stepid)      
    self.setName( '3. Optimization of the Segmentation' )
    self.setDescription( 'Optimize the level set segmentation' )


    
  def createUserInterface(self):
    self.__layout = self.__parent.createUserInterface()
    
    self.__spacerLabel = qt.QLabel(" ")      
    self.__layout.addRow(self.__spacerLabel)
      
#    self.__segmentationSectionLabel = qt.QLabel("Fix the Level-set Segmentation:")     
#    self.__layout.addRow(self.__segmentationSectionLabel)
      
    self.__ioAdvancedPanel = qt.QFrame(self)
    print "testss"
    self.__ioAdvancedPanel.setFrameStyle(6)
    self.__layout.addRow(self.__ioAdvancedPanel)
#    self.__ioAdvancedToggle.connect("clicked()", self.onIOAdvancedToggle) 
    
    ioAdvancedFormLayout = qt.QFormLayout(self.__ioAdvancedPanel)
          
      
    self.__buttonBox = qt.QDialogButtonBox() 
    self.__resetButton = self.__buttonBox.addButton(self.__buttonBox.RestoreDefaults)
    self.__resetButton.text = "Undersegmentation"
    self.__resetButton.toolTip = "Click to perfom an Undersegmentation."
    self.__previewButton = self.__buttonBox.addButton(self.__buttonBox.Discard)
    self.__previewButton.setIcon(qt.QIcon())
    self.__previewButton.text = "Oversegmentation"
    self.__previewButton.toolTip = "Click to perfom an Oversegmentation."
#      self.__startButton = self.__buttonBox.addButton(self.__buttonBox.Apply)
#      self.__startButton.setIcon(qt.QIcon())
#      self.__startButton.text = "Start!"
#      self.__startButton.enabled = False
#      self.__startButton.toolTip = "Click to start the filtering."
    ioAdvancedFormLayout.addWidget(self.__buttonBox)
      
      
  def validate(self, desiredBranchId):
    self.__parent.validate( desiredBranchId )

