import yaml
import sys
import os
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

    mseVals1 = compareMSE(data1)
    mseVals2 = compareMSE(data2)
    mseVals3 = compareMSE(data3)
    mseVals4 = compareMSE(data4)

    X = [1,2,3,4,5,6,7,8,9,10,11,12,13, 14]
    figure, axis = plt.subplots(2,2)


    axis[0, 0].plot(X, mseVals1,'--bo',color='blue')
    axis[0, 0].set_title("2022-1-B-openAI")
    
    # For Cosine Function
    axis[0, 1].plot(X, mseVals2,'--bo',color='blue')
    axis[0, 1].set_title("2022-1-B-bert")
    
    # For Tangent Function
    axis[1, 0].plot(X, mseVals3,'--bo',color='blue')
    axis[1, 0].set_title("2022-1-A-babbage")
    
    # For Tanh Function
    axis[1, 1].plot(X, mseVals4 ,'--bo',color='blue')
    axis[1, 1].set_title("to posledne")

    print(calcTotalMseError(data1))
    print(calcTotalMseError(data2))
    print(calcTotalMseError(data3))
    print(calcTotalMseError(data4))

    plt.show()