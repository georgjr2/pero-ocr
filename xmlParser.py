from pero_ocr.document_ocr.layout import PageLayout
import sys
colors = ["31", "32", "33", "34", "35", "36", "37"]
if __name__ == '__main__':
    # Create layout object
    layout = PageLayout(file = sys.argv[1])
    # Print layout object
    # print(layout)
    colorIndex = 0
    for region in layout.regions:
        print("\x1b[" + colors[colorIndex%7] + "m", region.get_region_transcription())
        colorIndex += 1
    print("\n")