from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import sys
import numpy as np
import yaml

def loadTranscriptions(file):
    with open(file, 'r', encoding="utf-8") as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded

def prepareBaseAnswers(data):
    baseAnswers = {}
    notRatedAnswers = {}
    for pageId in data:
        for answerId in data[pageId]['answers']:
            # skip incorrect answers with empty questions
            if not data[pageId]['questions'][answerId]:
                continue
            
            login = data[pageId]['login']
            answerText = data[pageId]['answers'][answerId]
            if len(data[pageId]['points']) > answerId:
                if data[pageId]['points'][answerId].isnumeric():
                    answerPoints = round(float(data[pageId]['points'][answerId]))
                else:
                    answerPoints = 0
            else:
                answerPoints = 0

            if answerId not in baseAnswers:
                baseAnswers[answerId] = []

            if len(baseAnswers[answerId]) <= 12:
                sameRating = False
                for questionBaseAnswers in baseAnswers[answerId]:
                    if questionBaseAnswers['baseRating'] == answerPoints:
                        sameRating = True
                        break
                if not sameRating:
                    baseAnswers[answerId].append({'text': answerText, 'baseRating': answerPoints})
                    continue

            if login not in notRatedAnswers:
                notRatedAnswers[login] = {}
            notRatedAnswers[login][answerId] = {'text': answerText, 'rating': 0, 'bestRating': 0, 'baseRating': answerPoints}

    return baseAnswers, notRatedAnswers

def rateAnswers(model,  baseAnswers, notRatedAnswers):
    for login in notRatedAnswers:
        for answerId in notRatedAnswers[login]:
            notRatedAnswer = notRatedAnswers[login][answerId]['text']
            mergedAnswers = [notRatedAnswer]
            for baseAnswer in baseAnswers[answerId]:
                mergedAnswers.append(baseAnswer['text'])
            sen_embeddings = model.encode(mergedAnswers)
            ratings = cos_sim(np.array([sen_embeddings[0]]), np.array(sen_embeddings[1:]))
            ratings = ratings[0]
            answerRating = 0
            bestRatingClass = 0
            bestRating = 0
            for i in range(0, len(ratings)):
                baseAnswerRating = baseAnswers[answerId][i]['baseRating']
                currentRating = float(ratings[i])
                answerRating += currentRating * float(baseAnswerRating)
                if currentRating > bestRating:
                    bestRating = currentRating
                    bestRatingClass = baseAnswerRating
            answerRating /= sum(ratings)
            notRatedAnswers[login][answerId]['rating'] = round(float(answerRating))
            notRatedAnswers[login][answerId]['bestRating'] = bestRatingClass
    return notRatedAnswers

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect args")

    data = loadTranscriptions(sys.argv[1])
    baseAnswers, notRatedAnswers = prepareBaseAnswers(data)

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    ratedAnswers = rateAnswers(model, baseAnswers, notRatedAnswers)

    with open('results.yaml','w') as yamlfile:
        dump = yaml.dump(ratedAnswers)
        yamlfile.write(dump)
