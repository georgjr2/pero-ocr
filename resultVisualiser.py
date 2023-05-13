import yaml
import sys
import os
import re
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def loadTranscriptions(file):
    with open(file, 'r', encoding="utf-8") as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded

def plotQuestionPoints(data, questionNum, ax):
    xArr = []
    yArr = []
    yArr2 = []
    cnt = 0
    for login in data:
        if questionNum in data[login]:
            xArr.append(cnt)
            yArr.append(float(data[login][questionNum]['truth']))
            yArr2.append(data[login][questionNum]['pred'])
            cnt += 1
    ax.plot(xArr, yArr, color='blue')
    ax.plot(xArr, yArr2, color='red')
            

def compareMSE(data):

    trueScore = []
    predictionScore = []
    mseValues = []

    for questionNum in range(1, 15):
        for login in data:
            #print(questionNum)
            if questionNum in data[login]:
                trueScore.append(float(data[login][questionNum]['truth']))
                predictionScore.append(data[login][questionNum]['pred'])
        mseValues.append(mean_squared_error(trueScore, predictionScore))
       
        questionNum +=1
    return mseValues


def getTestScoreMSE(data):

    trueTestScores = []
    predictionTestScores = []

    for login in data:
        trueScore = 0
        predictionScore = 0
        for questionNum in range(1, 15):
            if questionNum in data[login]:
                trueScore += float(data[login][questionNum]['truth'])
                predictionScore += data[login][questionNum]['pred']
        #print("truth: ", trueScore)
        #print("prediction:  ", predictionScore)
        trueTestScores.append(trueScore)
        predictionTestScores.append(predictionScore)
    return mean_squared_error(trueTestScores, predictionTestScores)
            
def plotTestPoints(data, ax):
    xArr = []
    yArr = []
    yArr2 = []
    cnt = 0
    for login in data:
        baseRatingSum = 0
        ratingSum = 0
        for questionNum in data[login]:
            baseRatingSum += float(data[login][questionNum]['truth'])
            ratingSum += data[login][questionNum]['pred']

        xArr.append(cnt)
        yArr.append(baseRatingSum)
        yArr2.append(ratingSum)
        cnt += 1
    ax.plot(xArr, yArr, color='blue')
    ax.plot(xArr, yArr2, color='red')

def calcTotalMseError(data):
    xArr = []
    yArr = []
    for login in data:
        for questionNum in data[login]:
            xArr.append(float(data[login][questionNum]['pred']))
            yArr.append(data[login][questionNum]['truth'])
    return mean_squared_error(xArr, yArr)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect args")

    data1 = loadTranscriptions(sys.argv[1])
    data2 = loadTranscriptions(sys.argv[2])
    data3 = loadTranscriptions(sys.argv[3])
    data4 = loadTranscriptions(sys.argv[4])
    data5 = loadTranscriptions(sys.argv[5])

    mseVals1 = compareMSE(data1)
    mseVals2 = compareMSE(data2)
    mseVals3 = compareMSE(data3)
    mseVals4 = compareMSE(data4)
    mseVals5 = compareMSE(data5)

    X = [1,2,3,4,5,6,7,8,9,10,11,12,13, 14]
    figure, axis = plt.subplots(3,2)


    axis[0, 0].plot(X, mseVals1,'--bo',color='blue')
    axisTitle  = os.path.basename(sys.argv[1])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[0, 0].set_title("Test 1 -- {} MSE".format(axisTitle))
    axis[0, 0].set_ylim(1,6)
    
    #
    axis[0, 1].plot(X, mseVals2,'--bo',color='blue')
    axisTitle  = os.path.basename(sys.argv[2])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[0, 1].set_title("Test 2 -- {} MSE".format(axisTitle))
    axis[0, 1].set_ylim(1,6)
    
    # 
    axis[1, 0].plot(X, mseVals3,'--bo',color='blue')
    axisTitle  = os.path.basename(sys.argv[3])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[1, 0].set_title("Test 3 -- {} MSE".format(axisTitle))
    axis[1, 0].set_ylim(1,6)
    
    # 
    axis[1, 1].plot(X, mseVals4 ,'--bo',color='blue')
    axisTitle  = os.path.basename(sys.argv[4])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[1, 1].set_title("Test 4 -- {} MSE".format(axisTitle))
    axis[1, 1].set_ylim(1,6)

    axis[2, 1].plot(X, mseVals5 ,'--bo',color='blue')
    axisTitle  = os.path.basename(sys.argv[5])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[2, 1].set_title("Test 5 -- {} MSE".format(axisTitle))
    axis[2, 1].set_ylim(1,6)

    """
    print(calcTotalMseError(data1))
    print(calcTotalMseError(data2))
    print(calcTotalMseError(data3))
    print(calcTotalMseError(data4))
    """
    testMse1 = getTestScoreMSE(data1)
    testMse2 = getTestScoreMSE(data2)
    testMse3 = getTestScoreMSE(data3)
    testMse4 = getTestScoreMSE(data4)
    testMse5 = getTestScoreMSE(data5)

    wholeTestMSE = []
    wholeTestMSE.append(testMse1)
    wholeTestMSE.append(testMse2)
    wholeTestMSE.append(testMse3)
    wholeTestMSE.append(testMse4)
    wholeTestMSE.append(testMse5)

    Xnew = ['test1', 'test2','test3','test4', 'test5']
    #MSE whole test
    axis[2, 0].plot(Xnew, wholeTestMSE ,'o',color='blue')
    axis[2, 0].set_title("MSE for the whole test")
    
    plt.show()