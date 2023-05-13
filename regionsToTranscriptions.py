from pero_ocr.document_ocr.layout import PageLayout
import yaml
import sys
import os

def getRegions(file):
    layout = PageLayout(file=file)
    return layout.regions

def getAnswersAndQuestions(data, file):
    answers = data[file]['answers']
    questions = data[file]['questions']

    regions = getRegions(os.path.join(sys.argv[2], file))

    answerText = {}
    questionText = {}

    for answerNum in iter(answers):
        answerRegions = answers[answerNum]

        texts = []
        for regionId in answerRegions:
            region = filter(lambda x: x.id == regionId, regions)
            if sum(1 for _ in region) != 1:
                raise Exception("Error, duplicate answer regions found:", list(region))
            region = next(filter(lambda x: x.id == regionId, regions))
            texts.append(region.get_region_transcription())
        answerText[answerNum] = ";".join(texts)

    for questionNum in iter(questions):
        questionRegions = questions[questionNum]

        texts = []
        for regionId in questionRegions:
            region = filter(lambda x: x.id == regionId, regions)
            if sum(1 for _ in region) != 1:
                raise Exception("Error, duplicate question regions found")
            region = next(filter(lambda x: x.id == regionId, regions))
            texts.append(region.get_region_transcription())
        questionText[questionNum] = ";".join(texts)
    return answerText, questionText

def getPoints(year, test, annFolder):
    fileAnnName = "body-{}_{}.txt.uniform.anon".format(year, test)
    annFile = os.path.join(annFolder, fileAnnName)
    with open(annFile) as f:
        lines = f.readlines()
        points = {}
        for line in lines:
            line = line.split()
            points[line[0]] = line[2:]
        return points

allPoints = {}

def parseYaml(file):
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    res = {}

    dataIt = iter(data)
    for file in dataIt:
        answerText, questionText = getAnswersAndQuestions(data, file)
        year = data[file]["year"]
        test = data[file]["test"]
        if not year+test in allPoints:
            allPoints[year+test] = getPoints(year, test, sys.argv[3])
        login = data[file]["login"]
        if login in allPoints[year+test]:
            points = allPoints[year+test][login]
        else:
            points = []
        res[file] = {
                "answers": answerText,
                "questions": questionText,
                "points": points,
                "year": year,
                "test": test,
                "login": login,
            }
    return res

def Merge(dict1, dict2):
    return(dict2.update(dict1))

if __name__ == '__main__':
    folder = sys.argv[1]
    yamlData = {}
    for file in os.listdir(folder):
        newDict = parseYaml(os.path.join(folder, file))
        Merge(yamlData, newDict)
        yamlData = newDict
        yamlOutputName = folder + 'transcripted.yaml'
    # print(yamlData)
    with open(yamlOutputName,'w') as yamlfile:
        yaml.dump(yamlData, yamlfile, default_flow_style=False, allow_unicode=True)
    print("Done")
