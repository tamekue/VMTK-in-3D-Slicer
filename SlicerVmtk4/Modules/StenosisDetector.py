from __main__ import vtk, qt, ctk, slicer
#
# Stenosis detector using VMTK based Tools
#
import StenosisDetectorWizard
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
    
      steps.append(StenosisDetectorWizard.InputStep('Input'))
      steps.append(StenosisDetectorWizard.VesselnessFilterStep('Vesselness Filter'))
      steps.append(StenosisDetectorWizard.LevelSetSegmentationStep('Level Set Segmentation'))
  #    steps.append(OptimizationStep('Optimization'))
      steps.append(StenosisDetectorWizard.CenterlineComputationStep('Centerline Computation'))
      steps.append(StenosisDetectorWizard.VisualizationStep('Detect Stenosis'))
      
      logic = SlicerVmtk4CommonLib.StenosisDetectorLogic()
    
      # Add transition associated to steps
      for i in range(len(steps) - 1):
        steps[i].setLogic(logic)
        self.workflow.addTransition(steps[i], steps[i + 1])
    
      self.workflow.start()
    
      workflowWidget.visible = True
      self.layout.addWidget(workflowWidget)    



