class EmotionDetector():
    def __init__(self):
        self.smiles = []
        self.eyes = []
        self.mouthHeights = []
        self.avgEmotion = 0
        self.numSmiles = len(self.smiles)

    def detectEmotion(self):
        self.numSmiles = len(self.smiles)
        if(self.numSmiles <= 0):
            return ""
        if self.detectSmile():
            self.avgEmotion +=1
            return "happy"
        if self.detectFrown():
            self.avgEmotion -=1
            return "sad"
        return "neutral"
    
    def getAvgEmotion(self):
        self.numSmiles = len(self.smiles)
        if(self.numSmiles <= 0):
            return ""
        if(self.avgEmotion/self.numSmiles > 0.1):
            return "happy"
        elif(self.avgEmotion/self.numSmiles < -0.1):
            return "sad"
        else:
            return "neutral"

    def detectSmile(self):
        smileAvg = sum(self.smiles)/self.numSmiles
        recentSmile = self.smiles[self.numSmiles-1]
        if(recentSmile>smileAvg*1.1): 
            return True
        return False
    
    def detectNeutral(self):
        smileAvg = sum(self.smiles)/self.numSmiles
        recentSmile = self.smiles[self.numSmiles-1]
        if(recentSmile<smileAvg*1.1 and recentSmile > smileAvg*0.97): 
            return True
        return False

    def detectFrown(self):
        smileAvg = sum(self.smiles)/self.numSmiles
        recentSmile = self.smiles[self.numSmiles-1]
        if(recentSmile<smileAvg*0.97): 
            return True
        return False
    
    def detectSurprise(self):
        eyeAvg = sum(self.eyes)/self.numSmiles
        mouthAvg = sum(self.mouthHeights)/self.numSmiles
        recentEye = self.eyes[self.numSmiles-1]
        recentMouth = self.mouthHeights[self.numSmiles-1]
        if(recentEye > eyeAvg and recentMouth > mouthAvg): 
            return True
        return False

    def addLandmarks(self, landmarkPoints):
        if(len(landmarkPoints) > 0):
            smileLength = landmarkPoints[54][0] - landmarkPoints[48][0]
            topEyeAvg = (landmarkPoints[38][1] + landmarkPoints[37][1] + 
                            landmarkPoints[43][1] + landmarkPoints[44][1])/4
            bottomEyeAvg = (landmarkPoints[41][1] + landmarkPoints[40][1] + 
                            landmarkPoints[46][1] + landmarkPoints[47][1])/4
            eyeHeight =  topEyeAvg - bottomEyeAvg
            mouthHeight = landmarkPoints[51][0] - landmarkPoints[57][0]
            self.smiles.append(smileLength)
            self.eyes.append(eyeHeight)
            self.mouthHeights.append(mouthHeight)
        