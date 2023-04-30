from pero_ocr.document_ocr.layout import PageLayout
import sys

if __name__ == '__main__':
    # Create layout object
    layout = PageLayout(file = sys.argv[1])
    # Print layout object
    # print(layout)
    for region in layout.regions:
        print(region.get_region_transcription())
        print(" ")
