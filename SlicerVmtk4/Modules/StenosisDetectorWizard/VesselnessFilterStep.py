from __main__ import qt, ctk
import PythonQt

import SlicerVmtk4CommonLib
from StenosisDetectorStep import *

class VesselnessFilterStep(StenosisDetectorStep) :
  """Step implemented using the derivation approach"""
  
  def __init__(self, stepid):
    self.__parent=super(VesselnessFilterStep, self)
    self.__parent.__init__(stepid)
    self.setName( '2. Vesselness Filter' )
    self.setDescription( 'Perform vessel enhancement of the loaded volume' )
        
    self.__inImageData = vtk.vtkImageData()
    self.__outImageData = None


    
  def createUserInterface(self):
    self.__layout = self.__parent.createUserInterface()
    
    self.__previewWindow = ctk.ctkVTKSliceView()   
      
    self.__previewHLayout = qt.QHBoxLayout()
    self.__previewHLayout.addWidget(self.__previewWindow)     
    self.__spaceLabel = qt.QLabel("                                    ")      
    self.__previewHLayout.addWidget(self.__spaceLabel)      
    self.__spaceLabel2 = qt.QLabel("                                   ")      
    self.__previewHLayout.addWidget(self.__spaceLabel2)      
    self.__layout.addRow(self.__previewHLayout)


# Frame slider
#    self.frameSlider = ctk.ctkSliderWidget()
#   frameSlider.connect('valueChanged(double)', self.frameSliderValueChanged)
#    self.frameSlider.decimals = 0
#    self.__layout.addRow("Preview for one Slicer: ", self.frameSlider)
           
                      
    self.__ioAdvancedToggle = qt.QCheckBox("Show Advanced")
    self.__ioAdvancedToggle.setChecked(False)
    self.__layout.addRow(self.__ioAdvancedToggle)
  

#
# I/O advanced panel
#
    self.__ioAdvancedPanel = qt.QFrame(self)
    self.__ioAdvancedPanel.hide()
    print "testss"
    self.__ioAdvancedPanel.setFrameStyle(6)
    self.__layout.addRow(self.__ioAdvancedPanel)
    self.__ioAdvancedToggle.connect("clicked()", self.onIOAdvancedToggle) 

    ioAdvancedFormLayout = qt.QFormLayout(self.__ioAdvancedPanel)
  
  
      # Frame delay slider
    self.frameDelaySlider = ctk.ctkRangeWidget()
  # frameDelaySlider.connect('valueChanged(double)', self.frameDelaySliderValueChanged)
    self.frameDelaySlider.decimals = 0
    self.frameDelaySlider.minimum = 1
    self.frameDelaySlider.maximum = 70
    self.frameDelaySlider.minimumValue = 5
    self.frameDelaySlider.maximumValue = 20
    self.frameDelaySlider.suffix = " vx"
#    self.frameDelaySlider.value = 20
    ioAdvancedFormLayout.addRow("Diameters [Min-Max]: ", self.frameDelaySlider)


   # Frame delay slider
    self.frameDelaySlider = ctk.ctkSliderWidget()
 # frameDelaySlider.connect('valueChanged(double)', self.frameDelaySliderValueChanged)
    self.frameDelaySlider.decimals = 0
    self.frameDelaySlider.minimum = 5
    self.frameDelaySlider.maximum = 100
    self.frameDelaySlider.value = 20
    ioAdvancedFormLayout.addRow("Input Contrast: ", self.frameDelaySlider)
    
    self.__previewButton=qt.QPushButton()
    self.__previewButton.text="Update preview"
#    self.__inputVolumeNodeSelector.setMRMLScene(slicer.mrmlScene)
    
    self.__previewButtonHLayout = qt.QHBoxLayout()
    self.__spaceLabel2 = qt.QLabel("                                   ")      
    self.__previewButtonHLayout.addWidget(self.__spaceLabel2)     
    self.__spaceLabel = qt.QLabel("                                    ")      
    self.__previewButtonHLayout.addWidget(self.__spaceLabel)      
    self.__previewButtonHLayout.addWidget(self.__previewButton)      
    self.__layout.addRow(self.__previewButtonHLayout)  
    self.__previewButton.connect("clicked()", self.updatePreview)   
        
  def validate(self, desiredBranchId):
    self.__parent.validate( desiredBranchId )
    print "#########################################  Validation!!!"
#    self.start()
    
    
  def onEntry(self, comingFrom, transitionType):    
    self.__parent.onEntry(comingFrom, transitionType)
    self.__inImageData.DeepCopy(self.__parent.logic().getImageData())
 #   self.__previewWindow.setImageData(self.__inImageData)
    


    
  def onIOAdvancedToggle(self):
    '''
    Show the I/O Advanced panel
    '''
    if self.__ioAdvancedToggle.checked:
      print "IOadv_if"
      self.__ioAdvancedPanel.show()
    else:
      print "IOadv_else"
      self.__ioAdvancedPanel.hide()
      
      
  def updatePreview(self):
            
    # Some standard and test values
    alpha = 0.3
    beta = 500
    contrast = 100
    minimumDiameter = 0.5
    maximumDiameter = 2.0
 
    outImage = vtk.vtkImageData()
    savedImage = vtk.vtkImageData()
    
    newVolumeNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLScalarVolumeNode")
    newVolumeNode.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(newVolumeNode)
    
    outImage.DeepCopy(self.logic().performFrangiVesselness(self.__inImageData, minimumDiameter, maximumDiameter, 5, alpha, beta, contrast))
    outImage.Update()            
    
    # in the outImage we want spacing 1,1,1 and origin 0,0,0
    # we save the correct values to the node
    outImage.SetSpacing([1,1,1])
    outImage.SetOrigin([0,0,0])
    
    newVolumeNode.SetAndObserveImageData(outImage)
    newVolumeNode.SetSpacing(self.__inImageData.GetSpacing())
    newVolumeNode.SetOrigin(self.__inImageData.GetOrigin())
    
    selectionNode = slicer.app.mrmlApplicationLogic().GetSelectionNode()
    selectionNode.SetReferenceSecondaryVolumeID(newVolumeNode.GetID())
    slicer.app.mrmlApplicationLogic().PropagateVolumeSelection()    

    # renew auto window/level for the output
    newVolumeNode.GetDisplayNode().AutoWindowLevelOff()
    newVolumeNode.GetDisplayNode().AutoWindowLevelOn()
    
    # show foreground volume
    numberOfCompositeNodes = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLSliceCompositeNode')
    for n in xrange(numberOfCompositeNodes):
      compositeNode = slicer.mrmlScene.GetNthNodeByClass(n, 'vtkMRMLSliceCompositeNode')
      if compositeNode:
              compositeNode.SetForegroundOpacity(1.0)
   
        
    savedImage.DeepCopy(outImage)
    savedImage.Update()
    savedImage.SetSpacing(self.__inImageData.GetSpacing())
    savedImage.SetOrigin(self.__inImageData.GetOrigin())
    self.logic().setImageData(savedImage)     
    
 