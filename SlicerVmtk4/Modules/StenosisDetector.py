from __main__ import vtk, qt, ctk, slicer
#
# Stenosis detector using VMTK based Tools
#
#from StenosisDetectorStep import StenosisDetectorStep
from InputStep import *
from VesselnessFilterStep import *
from LevelSetSegmentationStep import *
#from OptimizationStep import *
from CenterlineComputationStep import *
from VisualizationStep import *
from SlicerVmtk4CommonLib import *

class StenosisDetector:
  def __init__(self, parent):
    parent.title = "Stenosis Detector"
    parent.category = "Vascular Modeling Toolkit"
    parent.contributor = "Suares Tamekue <tamekue@bwh.harvard.edu>"
    parent.helpText = """dsfdsf"""
    parent.acknowledgementText = """sdfsdfdsf"""
    self.parent = parent


class StenosisDetectorWidget:
  def __init__(self, parent=None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()

    if not parent:
      self.setup()
      self.parent.show()
    
  def setup(self):
      self.workflow = ctk.ctkWorkflow()
      
    
      workflowWidget = ctk.ctkWorkflowStackedWidget()
      workflowWidget.setWorkflow(self.workflow)
    
      steps = []
    
      steps.append(InputStep('Input'))
      steps.append(VesselnessFilterStep('Vesselness Filter'))
      steps.append(LevelSetSegmentationStep('Level Set Segmentation'))
  #    steps.append(OptimizationStep('Optimization'))
      steps.append(CenterlineComputationStep('Centerline Computation'))
      steps.append(VisualizationStep('Detect Stenosis'))
      
      logic = SlicerVmtk4CommonLib.StenosisDetectorLogic()
    
      # Add transition associated to steps
      for i in range(len(steps) - 1):
        steps[i].setLogic(logic)
        self.workflow.addTransition(steps[i], steps[i + 1])
    
      self.workflow.start()
    
      workflowWidget.visible = True
      self.layout.addWidget(workflowWidget)    



