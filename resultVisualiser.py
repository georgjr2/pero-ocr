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


def comparePoints(data):
    trueScore = []
    predictionScore = []
    questionNum = 1
    max = 15

    for login in data:
        if questionNum < max:
            if questionNum in data[login]:
                trueScore.append(float(data[login][questionNum]['truth']))
                predictionScore.append(data[login][questionNum]['pred'])
                questionNum += 1
    return trueScore, predictionScore
            

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

    data = loadTranscriptions(sys.argv[1])
    fig, ax = plt.subplots()
    print(calcTotalMseError(data))
    
    plotQuestionPoints(data,5, ax)


    trueData, predData= comparePoints(data)
    X = [1,2,3,4,5,6,7,8,9,10,11,12,13, 14]
    figure, axis = plt.subplots()

    axis.plot(X, trueData, 'o',color='blue', label="true score")
    axis.plot(X, predData, 'o',color='red', label="prediction score")
    leg = axis.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, fancybox=True, shadow=True)

    plt.show()