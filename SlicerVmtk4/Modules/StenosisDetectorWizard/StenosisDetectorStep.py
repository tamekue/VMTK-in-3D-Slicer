from __main__ import qt, ctk
#import PythonQt

import SlicerVmtk4CommonLib
from StenosisDetector import *

class StenosisDetectorStep(ctk.ctkWorkflowWidgetStep) :
  """Step implemented using the derivation approach"""
  
  def __init__(self, stepid):
    self.initialize(stepid)
    self.__imageData = None
    self.__logic = None
    
  def logic(self):
      return self.__logic
  
  def setLogic(self,logic):      
      self.__logic = logic
    
  def createUserInterface(self):
#    layout = qt.QVBoxLayout(self)
    self.__layout = qt.QFormLayout( self )
#    label = qt.QLabel("This is %s" % self.id())
#    self.__layout.addWidget(label)
    return self.__layout
  
  def onEntry(self, comingFrom, transitionType):
    comingFromId = "None"
    if comingFrom: comingFromId = comingFrom.id()
    print "-> onEntry - current [%s] - comingFrom [%s]" % (self.id(), comingFromId)
    super(StenosisDetectorStep, self).onEntry(comingFrom, transitionType)
    
  def onExit(self, goingTo, transitionType):
    goingToId = "None"
    if goingTo: goingToId = goingTo.id()
    print "-> onExit - current [%s] - goingTo [%s]" % (self.id(), goingToId)
    super(StenosisDetectorStep, self).onExit(goingTo, transitionType)
    
  def validate(self, desiredBranchId):
    validationSuceeded = True
    print "-> validate %s" % self.id()
    
    super(StenosisDetectorStep, self).validate(validationSuceeded, desiredBranchId)

  def setImageData(self, imageData):
    print "inside of setImageData"
    self.__imageData = imageData
    print self.__imageData

  def getImageData(self):
    print "inside of getImageData"
    print self.__imageData
    return self.__imageData