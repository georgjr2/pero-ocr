from pero_ocr.document_ocr.layout import PageLayout
import os
import sys
colors = ["31", "32", "33", "34", "35", "36", "37"]
login = "3482488a15f00a9aad6021001c1ad921"

# argv1 = folder with xmls
# argv2 = folder with hashed logins
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 xmlParser.py <file>")
        sys.exit(1)
    folder = sys.argv[1]
    folderAnn = sys.argv[2]
    for file in os.listdir(folderAnn):
        if file.endswith(".hashed"):
            #open file
            with open(folderAnn + "/" + file, "r") as f:
                #find login in file
                for line in f:
                    if login in line:
                        print("foun login: " + line)

def getPageRegions(file):
    colorIndex = 0
    layout = PageLayout(file=file)
    for region in layout.regions:
        print("\x1b[" + colors[colorIndex%7] + "m", region.get_region_transcription())
        colorIndex += 1
    print("\n")
