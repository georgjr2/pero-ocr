import openai
import json
import numpy as np
import sys
from sklearn.metrics import mean_squared_error
from createTrainingForOpenAI import parseItem

def loadJson(file):
    with open(file, 'r', encoding="utf8") as json_file:
        data = json.load(json_file)
        return data

model = "babbage:ft-personal-2023-05-12-22-10-38"
data = loadJson(sys.argv[1])

import os
openai.api_key = os.environ["OPENAI_API_KEY"] 

y_true = []
y_pred = []
res = {}

def dumpRes():
    with open("babbage-05-12-22-10-38.yaml", 'w', encoding='utf8') as f:
        import yaml
        yaml.dump(res, f, allow_unicode=True)

import signal
def handler(signum, frame):
    print("\nMSE:", mean_squared_error(y_true, y_pred))
    dumpRes()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

def queryModel(prompt):
    return openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=1,
            logprobs=5,
    )

if __name__ == "__main__":
    i = 0
    import random
    random.shuffle(data)
    data = data[:500]
    for row in data:
        item = parseItem(row["questionTextRaw"], row["promptRaw"], row["completion"])
        prompt = item["prompt"] + "\n\n###\n\n"
        login = row["login"]
        promptRaw = row["promptRaw"].strip(";")
        questionNum = row["questionNum"]

        if row["completion"] == "0" or row["completion"] == "???":
            continue

        if not res.get(login):
            res[login] = {}

        i += 1

        completion = queryModel(prompt)

        if not completion["choices"][0]["text"].isnumeric():
            pred = "INVALID"
        else:
            pred = int(completion["choices"][0]["text"])

        true = int(float(row["completion"]))
        res[login][questionNum] = {"truth": true, "pred": pred, "text": promptRaw}

        # if abs(pred - true) > 2:
        #     print("expected:", row["completion"], "got:" , completion["choices"][0]["text"])
        #     print("answer:", row["prompt"])
        if pred == "INVALID":
            continue
        y_pred.append(pred)
        y_true.append(true)

        if i % 10 == 0:
            print("MSE:", mean_squared_error(y_true, y_pred))
    dumpRes()
    print("MSE:", mean_squared_error(y_true, y_pred))
