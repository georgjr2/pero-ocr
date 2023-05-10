import yaml
import json
import sys

questionsNum = 14

def loadTranscriptions(file):
     with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data

def getTranscriptionPointPair(page):
    if len(page["points"]) != questionsNum:
        print(Exception("Error, invalid number of points:", page["points"]))
        return
    res = []
    for idx in iter(page["answers"]):
        x = {"questionNum": idx+1, "promptRaw":  page["answers"][idx], "completion": page["points"][idx], "login": page["login"], "year": page["year"], "test": page["test"], "questionTextRaw": page["questions"][idx]}
        res.append(x)
    return res


if __name__ == "__main__":
    transcriptions = loadTranscriptions(sys.argv[1])
    trainingDatas = []
    for key in transcriptions:
        page = transcriptions[key]
        pageTranscriptions = getTranscriptionPointPair(page)
        if pageTranscriptions:
            trainingDatas.append(pageTranscriptions)
    with open("trainingData.json", 'w', encoding='utf8') as f:
        trainingData = [item for sublist in trainingDatas for item in sublist]
        json.dump(trainingData, f, ensure_ascii=False)
    print("Done")
