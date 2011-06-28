from __main__ import qt, ctk
import PythonQt

import SlicerVmtk4CommonLib
from StenosisDetectorStep import *

class CenterlineComputationStep(StenosisDetectorStep) :
  """Step implemented using the derivation approach"""
  
  def __init__(self, stepid):
    self.__parent=super(CenterlineComputationStep, self)
    self.__parent.__init__(stepid)      
    self.setName( '4. Centerline Computation' )
    self.setDescription( 'Compute the centerline' )

    
  def createUserInterface(self):
    self.__layout = self.__parent.createUserInterface()
    
    self.__spacerLabel = qt.QLabel(" ")      
    self.__layout.addRow(self.__spacerLabel)
      
      
                 
    self.__segmentationSectionLabel = qt.QLabel("Set seeds for vessel paths:")     
    self.__layout.addRow(self.__segmentationSectionLabel)
      
      
    self.__spacerLabel = qt.QLabel(" ")      
    self.__layout.addRow(self.__spacerLabel)
     
    self.__ioAdvancedPanel = qt.QFrame(self)
    print "testss"
    self.__ioAdvancedPanel.setFrameStyle(6)
    self.__layout.addRow(self.__ioAdvancedPanel)
#    self.__ioAdvancedToggle.connect("clicked()", self.onIOAdvancedToggle) 
    
  #  ioAdvancedFormLayout = qt.QFormLayout(self.__ioAdvancedPanel)
     
    # seed selector
    self.__seedFiducialsNodeSelector = slicer.qMRMLNodeComboBox()
    self.__seedFiducialsNodeSelector.objectName = 'seedFiducialsNodeSelector'
    self.__seedFiducialsNodeSelector.toolTip = "Select a hierarchy containing the fiducials to use as Seeds."
    self.__seedFiducialsNodeSelector.nodeTypes = ['vtkMRMLAnnotationFiducialNode']
    self.__seedFiducialsNodeSelector.baseName = "Start Seed"
    self.__seedFiducialsNodeSelector.noneEnabled = False
    self.__seedFiducialsNodeSelector.addEnabled = False
    self.__seedFiducialsNodeSelector.removeEnabled = False
    self.__layout.addRow("Start Seed: ", self.__seedFiducialsNodeSelector)
    self.connect('mrmlSceneChanged(vtkMRMLScene*)',
                       self.__seedFiducialsNodeSelector, 'setMRMLScene(vtkMRMLScene*)')   
#    self.__seedFiducialsNodeSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSeedChanged)
    
     
    self.__spacerLabel = qt.QLabel(" ")      
    self.__layout.addRow(self.__spacerLabel)
     
     
     # seed selector
    self.__targetSeedFiducialsNodeSelector = slicer.qMRMLNodeComboBox()
    self.__targetSeedFiducialsNodeSelector.objectName = 'seedFiducialsNodeSelector'
    self.__targetSeedFiducialsNodeSelector.toolTip = "Select a hierarchy containing the fiducials to use as Seeds."
    self.__targetSeedFiducialsNodeSelector.nodeTypes = ['vtkMRMLAnnotationHierarchyNode']
    self.__targetSeedFiducialsNodeSelector.baseName = "Target Seeds"
    self.__targetSeedFiducialsNodeSelector.noneEnabled = False
    self.__targetSeedFiducialsNodeSelector.addEnabled = False
    self.__targetSeedFiducialsNodeSelector.removeEnabled = False
    self.__layout.addRow("Target Seeds: ", self.__targetSeedFiducialsNodeSelector)
    self.connect('mrmlSceneChanged(vtkMRMLScene*)',
                      self.__targetSeedFiducialsNodeSelector, 'setMRMLScene(vtkMRMLScene*)')   
#    self.__targetSeedFiducialsNodeSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSeedChanged)
          
    
    self.__seedFiducialsNodeSelector.setMRMLScene(slicer.mrmlScene)
    self.__targetSeedFiducialsNodeSelector.setMRMLScene(slicer.mrmlScene)
    
      
  def validate(self, desiredBranchId):
    self.__parent.validate( desiredBranchId )

        
  def restoreDefaults(self):
      pass
  
  
  def onRefreshButtonClicked(self):  
      pass
