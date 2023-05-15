# Automatic answer grading using transformers
## Authors: xmarti97, xharva03, xtizsa00

questionSeparator.py - uses templates to extract transcriptions
regionsToTranscriptions.py - extracts output from questionSeparator, and creates raw dataset with paired grades, logins, and other metadata
createTrainingData.py - takes from data regionsToTranscriptions, and creates it monolytic json dataset containing prompt and completions
createTrainingDataForOpenAI.py - takes json training data, and creates complete promps
calculateLoss.py - creates .yaml results from OpenAI, which can be evaluated via resultVisualiser.py
answerSimilarityEval.py - uses bert for result evalation (instead of openai)
resultVisualiser.py - visualises results from calculateLoss and answerSimilarityEval.py
