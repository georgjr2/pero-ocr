import json
import sys
import random

def loadJson(file):
     with open(file) as f:
        data = json.load(f)
        return data

def getRandomOtherThen(questionNum, data):
    res = []
    while len(res) < 2:
        item = random.choice(data)
        if item["questionNum"] != questionNum:
            res.append(item)
    return res

def parseItem(question, answer, completion, questionNum):
    answer = answer.strip(";")
    question = question.strip(";")
    prompt = "For question: " + question + " , grade answer (from 0 to 4): " + answer
    return {"prompt": prompt, "completion": completion}

if __name__ == "__main__":
    data = loadJson(sys.argv[1])
    final = []
    for item in data:
        if item["completion"] == "???":
            continue
        item["completion"] = str(int(float(item["completion"])))
        final.append(parseItem(item["questionTextRaw"], item["promptRaw"], item["completion"], item["questionNum"]))
        others = getRandomOtherThen(item["questionNum"], data)
        for other in others:
            final.append(parseItem(item["questionTextRaw"], other["promptRaw"], "0", item["questionNum"]))
    with open("trainingDataOPENAI.json", 'w', encoding='utf8') as f:
        json.dump(final, f, ensure_ascii=False)
    print("Done")
