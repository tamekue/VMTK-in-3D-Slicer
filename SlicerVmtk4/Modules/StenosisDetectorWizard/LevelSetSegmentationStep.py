from __main__ import qt, ctk
import PythonQt

import SlicerVmtk4CommonLib
from StenosisDetectorStep import *

class LevelSetSegmentationStep(StenosisDetectorStep) :
  """Step implemented using the derivation approach"""
  
  def __init__(self, stepid):
    self.initialize(stepid)
    self.setName( '3. Optimization of the Segmentation' )
    self.setDescription( 'Optimize the level set segmentation' )
    self.__parent=super(LevelSetSegmentationStep, self)
    self.__inImageData = vtk.vtkImageData()
    self.__outImageData = None
    # the pointer to the logic
    self.__logic = None    

    
  def createUserInterface(self):
    self.__layout = self.__parent.createUserInterface()
    
    self.__spacerLabel = qt.QLabel(" ")      
    self.__layout.addRow(self.__spacerLabel)
      
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
    print "#########################################  Validatione!!!"


  def onEntry(self, comingFrom, transitionType):    
    self.__parent.onEntry(comingFrom, transitionType)
    self.__inImageData.DeepCopy(self.__parent.logic().getImageData())
    self.start()
     
    
  def start(self):
              
#    self.__thresholdSlider.minimum = 0
#    self.__thresholdSlider.maximum = 100
#    self.__thresholdSlider.minimumValue = 0
#    self.__thresholdSlider.maximumValue = 100
#    self.__thresholdSlider.singleStep = 1

#    self.__ioAdvancedToggle.setChecked(False)
#    self.__segmentationAdvancedToggle.setChecked(False)
#    self.__ioAdvancedPanel.hide()
#    self.__segmentationAdvancedPanel.hide()

    stoppers = vtk.vtkIdList()
    
#    self.__inflationSlider.value = 0
#    self.__curvatureSlider.value = 70
#    self.__attractionSlider.value = 50    
#    self.__iterationSpinBox.value = 10

    # initialization
    initImageData = vtk.vtkImageData()    
    # evolution
    evolImageData = vtk.vtkImageData()
    # saved image
    segmetedImage = vtk.vtkImageData()
    
    newVolumeNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLScalarVolumeNode")
    newVolumeNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(newVolumeNode)
    
    
    inputImage = vtk.vtkImageData()  
    inputImage.DeepCopy(self.__inImageData)
    # perform the initialization
    initImageData.DeepCopy(self.GetLogic().performInitialization(inputImage,
                                                                 0,
                                                                 100,
                                                                 self.GetLogic().getOutputIds(),
                                                                 stoppers,
                                                                 0)) # TODO sidebranch ignore feature
    initImageData.Update()
    
    
      
  #  evolImageData.DeepCopy(self.GetLogic().performEvolution(self.__inImageData,
 #                                                               initImageData,
 #                                                               10,
 #                                                               0,
 #                                                               70,
 #                                                               50,
 #                                                               'geodesic'))
        
#    evolImageData.Update()
    
    newVolumeNode.SetAndObserveImageData(initImageData)
    
    newVolumeNode.SetAndObserveImageData(initImageData)
    newVolumeNode.SetModifiedSinceRead(1)
    newVolumeNode.Modified()
    
    selectionNode = slicer.app.mrmlApplicationLogic().GetSelectionNode()
    selectionNode.SetReferenceSecondaryVolumeID(newVolumeNode.GetID())
    slicer.app.mrmlApplicationLogic().PropagateVolumeSelection()    

    # renew auto window/level for the output
    newVolumeNode.GetDisplayNode().AutoWindowLevelOff()
    newVolumeNode.GetDisplayNode().AutoWindowLevelOn()
        
    segmetedImage.DeepCopy(initImageData)
    segmetedImage.Update()
    self.GetLogic().setImageData(segmetedImage)     
    
 
    
    
  def GetLogic(self):
    '''
    '''
    if not self.__logic:
        
        self.__logic = self.__parent.logic()
        
    return self.__logic
    
    