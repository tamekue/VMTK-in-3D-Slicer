SET(StenosisDetectorWizard_PYTHON_SCRIPTS
  __init__.py
  StenosisDetectorStep.py
  InputStep.py
  VesselnessFilterStep.py
  LevelSetSegmentationStep.py
  CenterlineComputationStep.py
  VisualizationStep.py
  # here go other vmtk logic classes
  )

SET(StenosisDetectorWizard_PYTHON_RESOURCES
  )
  
ctkMacroCompilePythonScript(
  TARGET_NAME StenosisDetectorWizard
  SCRIPTS "${StenosisDetectorWizard_PYTHON_SCRIPTS}"
  RESOURCES "${StenosisDetectorWizard_PYTHON_RESOURCES}"
  DESTINATION_DIR ${CMAKE_BINARY_DIR}/${Slicer_QTSCRIPTEDMODULES_LIB_DIR}/StenosisDetectorWizard
  INSTALL_DIR ${Slicer_QTSCRIPTEDMODULES_LIB_DIR}
  )

#-----------------------------------------------------------------------------
# Testing
#
if(BUILD_TESTING)
endif(BUILD_TESTING)
