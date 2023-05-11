import openai
import json
import numpy as np
import sys
from sklearn.metrics import mean_squared_error

def loadJson(file):
    with open(file, 'r') as json_file:
        return list(json_file)

model = "ada:ft-personal-2023-05-11-20-50-52"
data = loadJson(sys.argv[1])

import os
openai.api_key = os.environ["OPENAI_API_KEY"] 


y_true = []
y_pred = []

import signal
def handler(signum, frame):
    print("\nMSE:", mean_squared_error(y_true, y_pred))
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


if __name__ == "__main__":
    i = 0
    for row in data:
        row = json.loads(row)
        if row["completion"] == "0":
            continue
        i += 1
        completion = openai.Completion.create(
            model=model,
            prompt=row["prompt"],
            max_tokens=1,
            logprobs=5,
        )
        # print("expected:", row["completion"], "got:" , completion["choices"][0]["text"])
        logprobs = completion["choices"][0]["logprobs"]["top_logprobs"]
        # convert logprobs to probabilities
        if not row["completion"].isnumeric():
            continue
        y_pred.append(int(completion["choices"][0]["text"]))
        y_true.append(int(row["completion"]))
        if i % 10 == 0:
            print("MSE:", mean_squared_error(y_true, y_pred))
    print("MSE:", mean_squared_error(y_true, y_pred))
