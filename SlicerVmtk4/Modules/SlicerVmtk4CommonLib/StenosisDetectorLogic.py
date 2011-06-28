# vtk includes
from __main__ import vtk

from VesselnessFilteringLogic import *
from LevelSetSegmentationLogic import *
from CenterlineComputationLogic import *


class StenosisDetectorLogic(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # import the vmtk libraries

        self.__imageData = None
        self.__outputIds = None
        self.__logic = None
        
        self.__vesselnessLogic = None
        self.__levelsetLogic = None
        self.__centerlineLogic = None
          
          
    def vesselnessLogic(self):
        '''
        '''
        if not self.__vesselnessLogic:
        
            self.__vesselnessLogic = VesselnessFilteringLogic()
        
        return self.__vesselnessLogic
    
    def levelSetLogic(self):
        '''
        '''
        if not self.__levelsetLogic:
        
            self.__levelsetLogic = LevelSetSegmentationLogic()
        
        return self.__levelsetLogic
    
    def centerlineLogic(self):
        '''
        '''
        if not self.__centerlineLogic:
        
            self.__centerlineLogic = CenterlineComputationLogic()
        
        return self.__centerlineLogic
 
        
        
 #   def callFrangiVesselnessFilter(self, image, minimumDiameter, maximumDiameter, discretizationSteps, alpha, beta, gamma):
 #       '''
 #       '''
 #       print "###################################  performFrangiVesselness"
      #  outImage = vtk.vtkImageData()
      #  outImage =  self.GetLogic.performFrangiVesselness(image, minimumDiameter, maximumDiameter, discretizationSteps, alpha, beta, gamma)
                
 #       return self.GetLogic.performFrangiVesselness(image, minimumDiameter, maximumDiameter, discretizationSteps, alpha, beta, gamma)

    def performFrangiVesselness(self, image, minimumDiameter, maximumDiameter, discretizationSteps, alpha, beta, gamma):
        '''
        '''
        print "###################################  performing FrangiVesselness"

        return self.vesselnessLogic().performFrangiVesselness(image, minimumDiameter, maximumDiameter, discretizationSteps, alpha, beta, gamma)


    def performInitialization(self, image, lowerThreshold, upperThreshold, sourceSeedIds, targetSeedIds, ignoreSideBranches=0):
        '''
        '''
        return self.levelSetLogic().performInitialization(image, lowerThreshold, upperThreshold, sourceSeedIds, targetSeedIds, ignoreSideBranches)



    
    def performEvolution(self,originalImage,segmentationImage,numberOfIterations,inflation,curvature,attraction,method='geodesic'):
        '''
        
        '''
        print "###################################  performing Evolution"
        self.levelSetLogic().performEvolution(originalImage,segmentationImage,numberOfIterations,inflation,curvature,attraction,method)



    def GetStenosis(self,polyData):
        
        # here comes code
        self._parentClass.GetHelper().debug("This is ein test")

#my_inputdata=[[12,1,1,5], [4,8,1,6], [11,10,3,7], [14,21,3,7], [4,0,3,3], [11,10,3,3], [14,21,3,2], [12,1,1,4], [4,8,1,2],  [4,8,1,3], [11,10,3,3], [11,10,3,4], #[14,21,3,5],  [14,21,3,5]]
        my_outputdata=[];
        my_stenosisList=[];
        threshold = 0.60;
        lastMeasuredDiameter=4;
        statuschange=0;
        stenosisSegment=0;  # 0 = no in a stenosis segment    1 = in a stenosis segment   2 =
        detailsArray =[];
        diameter=0;
        radiusArray = polyData.GetPointData().GetArray("MaximumInscribedSphereRadius") 
        fList = slicer.MRMLScene.CreateNodeByClass('vtkMRMLFiducialListNode')
        slicer.MRMLScene.AddNode(fList)

        fList.SetGlyphType(12)
        fList.SetTextScale(0)

        for i in range(polyData.GetNumberOfPoints()):
            point = polyData.GetPoint(i)
            diameter = radiusArray.GetComponent(i,0) 

            if diameter < threshold: 
                if lastMeasuredDiameter >= threshold:
                    statuschange = 1
                else: statuschange = 0                    
                stenosisSegment=1  
                fList.AddFiducialWithXYZ(point[0],point[1],point[2],0)
                my_outputdata.append([point[0], point[1], point[2], diameter])        
                
            elif diameter >= threshold:                
                if lastMeasuredDiameter >= threshold:
                    statuschange = 0
                else: statuschange = 1
                stenosisSegment=0
                
            if statuschange ==1 and stenosisSegment==0:
                # End of a stenosis segment:
                # add the stenosis to the container and reset my_outputdata.
                my_stenosisList.append(my_outputdata);
                self._parentClass.GetHelper().debug("Stenosis ==> "+str(my_outputdata))
                my_outputdata = []  
            lastMeasuredDiameter = diameter             
        self._parentClass.GetHelper().debug("")
        self._parentClass.GetHelper().debug("Stenosis container: "+ str(my_stenosisList))
        self._parentClass.GetHelper().debug("Count: " + str(len(my_stenosisList)))
        
        
        
##################### Caculatting the current diameter...

    def GetDiameter_logic(self, data, seedPoint):        
        self._parentClass.GetHelper().debug("getDiameter:begin..")
   #     self._parentClass.laplaceFilter()
        
        #getting seed point coordinates
        for a in xrange(40):
            self._parentClass.GetHelper().debug("a: "+ str(a))
            currentCube = self.buildCurrentCube(seedPoint[0], seedPoint[1], seedPoint[2], a)
            for list in currentCube:
                if self.limitReached(list[0], list[1], list[2], data, seedPoint):
                    diameter = self.calculateDiameter(seedPoint[0], seedPoint[1], seedPoint[2], list[0], list[1], list[2], data, seedPoint)
                    self._parentClass.GetHelper().debug("diameter: "+ str(diameter))
                    return diameter
                else:
                    pass        
        #self._parentClass.GetHelper().debug("data : "+ str(data))
        return -1



    def buildCurrentCube(self, x,y,z,a):
        r = x+a
        s = y+a
        t = z+a
        u = x-a
        v = y-a
        w = z-a 
        currentCube = [ [x, y, t], [x, y, w], [x, s, z], [x, s, t], [x, s, w], [x, v, z], [x, v, t], [x, v, w],
               [r, y, z], [r, y, t], [r, y, w], [r, s, z], [r, s, t], [r, s, w], [r, v, z], [r, v, t], [r, v, w],
               [u, y, z], [u, y, t], [u, y, w], [u, s, z], [u, s, t], [u, s, w], [u, v, z], [u, v, t], [u, v, w]];
               
       #currentCube = [ [x, y, z+a], [x, y, z-a], [x, y+a, z], [x, y+a, z+a], [x, y+a, z-a], [x, y-a, z], [x, y-a, z+a], [x, y-a, z-a]
       #       [x+a, y, z], [x+a, y, z+a], [x+a, y, z-a], [x+a, y+a, z], [x+a, y+a, z+a], [x+a, y+a, z-a], [x+a, y-a, z], [x+a, y-a, z+a], [x+a, y-a, z-a]
         #      [x-a, y, z], [x-a, y, z+a], [x-a, y, z-a], [x-a, y+a, z], [x-a, y+a, z+a], [x-a, y+a, z-a], [x-a, y-a, z], [x-a, y-a, z+a], [x-a, y-a, z-a]];
        return currentCube;
                    
                    
    def limitReached(self, x, y, z, data, seedPoint):
        #return getValue(x,y,z)*getValue(seedPoint[0], seedPoint[1], seedPoint[2]) < 0
        self._parentClass.GetHelper().debug("x: "+ str(x)+" y: "+ str(y)+" z: "+ str(z))
        self._parentClass.GetHelper().debug("seedPoint_x: "+ str(seedPoint[0])+" seedPoint_y: "+ str(seedPoint[1])+" seedPoint_z: "+ str(seedPoint[2]))
        self._parentClass.GetHelper().debug("ptValue1: "+ str(data[x,y,z])+" ptValue2: "+ str(data[seedPoint[0], seedPoint[1], seedPoint[2]]))
        result = data[x,y,z]*data[seedPoint[0], seedPoint[1], seedPoint[2]]
        self._parentClass.GetHelper().debug("multiplication result: "+ str(result))
        
        if result < 0:
            return True
        else: 
            return False
            
                
    def calculateDiameter(self, a, b, c, x, y, z, data, seedPoint):
        checkResult = False
        q=0
        while not checkResult:
            q= q+1
            d = (2+q/10)*(a-x)+x
            e = (2+q/10)*(b-y)+y
            f = (2+q/10)*(c-z)+z
            checkResult= self.limitReached(d, e, f, data, seedPoint)
        
        if checkResult: 
            return self.calculateDistance(d, e, f, x, y, z)
        else: 
            return -1
        
        
    def calculateDistance(self, x, y, z, a, b, c):
        
        fList = slicer.MRMLScene.CreateNodeByClass('vtkMRMLFiducialListNode')
        slicer.MRMLScene.AddNode(fList)
        #fList.SetGlyphType(12)
        fList.SetTextScale(0)
        fList.AddFiducialWithXYZ( x, y, z, 0)
        fList.AddFiducialWithXYZ(a, b, c, 0)
        self._parentClass.GetHelper().debug("calculateDistance...")
        
        f = math.pow( (x-a), 2 )
        f += math.pow( (y-b), 2 )
        f += math.pow( (z-c), 2 )
        return  math.sqrt(f)
    
    
    def laplaceFilter(self, imageData ):

        g = slicer.vtkImageGaussianSmooth()
        g.SetInput(imageData)
        g.SetDimensionality(3)
        g.SetRadiusFactor(5)
        g.SetStandardDeviation(1.5)
        g.Update()

        l = slicer.vtkImageLaplacian()
        l.SetInput(g.GetOutput())
        l.Update()
        newImageData = slicer.vtkImageData() 
        newImageData.DeepCopy(l.GetOutput())
        return newImageData


    
    
    def setImageData(self, imageData):
      print "inside of setImageData"
      self.__imageData = imageData
      print self.__imageData
    
    def getImageData(self):
      print "inside of getImageData"
      print self.__imageData
      return self.__imageData    
  
    def setOutputIds(self, outputIds):
      print "inside of setOutputIds"
      self.__outputIds = outputIds
      print self.__outputIds
    
    def getOutputIds(self):
      print "inside of getOutputIds"
      print self.__outputIds
      return self.__outputIds
  
  
