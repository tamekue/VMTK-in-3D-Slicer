from __main__ import qt, ctk
import PythonQt

import SlicerVmtk4CommonLib
from StenosisDetectorStep import *

class InputStep(StenosisDetectorStep) :
  """Step implemented using the derivation approach"""
  
  def __init__(self, stepid):
    self.initialize(stepid)
    self.setName( '1. Input' )
    self.setDescription( 'Input for Volume and seed' )
    self.__parent=super(InputStep, self)
    
    # the pointer to the logic
    self.__logic = None    
    self.__parent.__init__(stepid)

    
  def createUserInterface(self):
    print "createUserInterface - InputStep"
    self.__layout = self.__parent.createUserInterface()    
    
    self.__spacerLabel = qt.QLabel(" ")      
    self.__layout.addRow(self.__spacerLabel)
    
       # inputVolume selector
    self.__inputVolumeNodeSelector = slicer.qMRMLNodeComboBox()
    self.__inputVolumeNodeSelector.objectName = 'inputVolumeNodeSelector'
    self.__inputVolumeNodeSelector.toolTip = "Select the input volume."
    self.__inputVolumeNodeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__inputVolumeNodeSelector.noneEnabled = False
    self.__inputVolumeNodeSelector.addEnabled = False
    self.__inputVolumeNodeSelector.removeEnabled = False
    self.__inputVolumeNodeSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", "0" )    
    self.__layout.addRow("Input Volume: ", self.__inputVolumeNodeSelector)
    self.connect('mrmlSceneChanged(vtkMRMLScene*)',
                       self.__inputVolumeNodeSelector, 'setMRMLScene(vtkMRMLScene*)')
#    self.__inputVolumeNodeSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onInputVolumeChanged)
    
         
    # seed selector
    self.__seedFiducialsNodeSelector = slicer.qMRMLNodeComboBox()
    self.__seedFiducialsNodeSelector.objectName = 'seedFiducialsNodeSelector'
    self.__seedFiducialsNodeSelector.toolTip = "Select a hierarchy containing the fiducials to use as Seeds."
    self.__seedFiducialsNodeSelector.nodeTypes = ['vtkMRMLAnnotationFiducialNode']
    self.__seedFiducialsNodeSelector.baseName = "Seeds"
    self.__seedFiducialsNodeSelector.noneEnabled = False
    self.__seedFiducialsNodeSelector.addEnabled = False
    self.__seedFiducialsNodeSelector.removeEnabled = False
    self.__layout.addRow("Seed: ", self.__seedFiducialsNodeSelector)
    self.connect('mrmlSceneChanged(vtkMRMLScene*)',
                       self.__seedFiducialsNodeSelector, 'setMRMLScene(vtkMRMLScene*)')   
#    self.__seedFiducialsNodeSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSeedChanged)
    

    self.__inputVolumeNodeSelector.setMRMLScene(slicer.mrmlScene)
    self.__seedFiducialsNodeSelector.setMRMLScene(slicer.mrmlScene)
        
    
  def validate(self, desiredBranchId):
    self.__parent.validate( desiredBranchId )
    self.start()
          
  def onIODiameterToggle(self):
    '''
    Show the I/O Advanced panel
    '''
    if self.__autoDiameter.checked:
      print "IOadv_if"
      self.__ioDiameterPanel.setEnabled(False)
      self.__enteredDiameter.setChecked(False)
      
    if self.__enteredDiameter.checked:
      print "IOadv_if"
      self.__ioDiameterPanel.setEnabled(True)
      self.__autoDiameter.setChecked(False)
      
  
  def start(self):
    '''
    '''
    SlicerVmtk4CommonLib.Helper.Debug("Starting Vesselness Filtering..")

    currentVolumeNode = self.__inputVolumeNodeSelector.currentNode()
    currentSeedsNode = self.__seedFiducialsNodeSelector.currentNode()
    image = currentVolumeNode.GetImageData()
    
    # standard values
    alpha = 0.3
    beta = 500
    contrast = 100
    minimumDiameter = 0.5
    maximumDiameter = 2.0
    contrast = 20
    outImage = vtk.vtkImageData()
    seeds = vtk.vtkIdList()
    
    #outImage.DeepCopy(self.GetLogic().performFrangiVesselness(image, minimumDiameter, maximumDiameter, 5, alpha, beta, contrast))
    outImage.DeepCopy(image)
    outImage.Update()
    self.GetLogic().setImageData(outImage)     

    # converting fiducials to vtkIdLists and sending to the logic
    seeds = SlicerVmtk4CommonLib.Helper.convertFiducialHierarchyToVtkIdList(currentSeedsNode, currentVolumeNode)
    self.GetLogic().setOutputIds(seeds)     
    
  def GetLogic(self):
    '''
    '''
    if not self.__logic:
        
        self.__logic = self.__parent.logic()
        
    return self.__logic
    
    
