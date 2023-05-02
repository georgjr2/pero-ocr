# for region in layout.regions:
#         print(region.polygon)
#         xs, ys = zip(*region.polygon)
#         plt.plot(xs,ys) 
#         print(region.get_region_transcription())
#         plt.text(xs[0], ys[0], region.get_region_transcription())
#     plt.show() 

from pero_ocr.document_ocr.layout import PageLayout
import os
import sys
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

login = "3482488a15f00a9aad6021001c1ad921"

question1 = [(122,390), (2430,357), (2430, 580), (122, 658), (122,390)]
answer1 = [(120, 1639), (2436, 1576), (2434, 647), (120, 680), (120, 1639)]

question2 = [(31, 1650), (2360, 1580), (2360, 1965), (80, 2022), (31, 1650)]
answer2 = [(42, 2075), (2405, 2011), (2400, 3315), (45, 3290), (42, 2075)]

polygons = [question1, answer1, question2, answer2]
color = ['red', 'green', 'black', 'orange']

# argv1 = folder with xmls
# argv2 = folder with hashed logins
class Person:
    def __init__(self, id, examHashs):
        self.id = id
        self.examHashs = [examHashs]
    def __str__(self):
        return f"<Id:{self.id} Hash:{self.examHashs}>"
    def __repr__(self):
        return f"<Id:{self.id} Hash:{self.examHashs}>"

persons = []

def getPageRegions(file):
    layout = PageLayout(file=file)
    
    for region in layout.regions:
        max = 0
        index = 0
        for i in range(0, len(polygons)):
            p = Polygon(polygons[i])
            q = Polygon(region.polygon)
            area = p.intersection(q).area
            if area > max:
                max = area
                index = i
        if max > 0:
            polygonColor = color[index]
        else: 
            polygonColor = 'yellow'
        xs, ys = zip(*region.polygon)
        plt.plot(xs,ys, color=polygonColor) 
        plt.text(xs[0], ys[0], region.get_region_transcription())

        #print(region.get_region_transcription())
        
    plt.show() 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 xmlParser.py <file>")
        sys.exit(1)
    print(sys.argv)
    folder = sys.argv[1]
    fileAnn = sys.argv[2]
    with open(fileAnn) as f:
        #find login in file
        for line in f:
            lineSplit = line.split()
            found = False
            for person in persons:
                if person.id == lineSplit[1]:
                    person.examHashs.append(lineSplit[0])
                    found = True
                    break
            if found == False:
                persons.append(Person(lineSplit[1], lineSplit[0]))
                #getPageRegions(line)
    for file in os.listdir(folder):
        if persons[0].examHashs[0] in file:
            getPageRegions(folder + file)