import csv
import json
import os
import sys
import getopt
import pathlib
import traceback

inputPath = ''
destPath = ''
sep = ''
enc = 'utf-8'


def csv_to_json(sep, csvFilePath, jsonFilePath, encodeType):

    jsonArray = []

    with open(csvFilePath, 'r', encoding=encodeType) as csvf:
        csvReader = csv.DictReader(
            csvf, delimiter=sep, quoting=csv.QUOTE_NONE)

        for row in csvReader:
            jsonArray.append(row)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


def process_file(filePath):
    fileExtension = pathlib.Path(filePath).suffix
    fileName = pathlib.Path(filePath).stem
    inputDirName = pathlib.Path(filePath).parent
    inputFullPath = os.path.join(inputDirName, fileName + fileExtension)
    destFullPath = os.path.join(inputDirName, fileName+'.json')

    # checking if it is a file and potentially valid for conversion
    # print(fullPath)
    if os.path.isfile(inputFullPath) and fileExtension in ('.csv', '.txt', '.prn'):
        # print('JSON:',os.path.join(fileDest,fileName+'.json'))
        try:
            csv_to_json(sep, inputFullPath, destFullPath, enc)
        except Exception:
            print(
                f'Cannot convert \"{inputFullPath}\". \n', traceback.format_exc())
    else:
        print(f'Cannot process {inputFullPath}.')


def main(argv):
    '''
    csv-to-json.py -s <separator> -i <path>

    JSON files are created in the same folder as <path>
    '''

    # fetch global vars
    global inputPath, destPath, sep, enc

    opts, args = getopt.getopt(
        argv, "hs:i:e:", ["separator=", "input=", "encoding="])
    for opt, arg in opts:
        if opt == '-h':
            print(main.__doc__)
            sys.exit()
        elif opt in ("-s", "--separator"):
            # arg need to be decoded to handle escaped character delimiter like tab
            sep = bytes(arg, "utf-8").decode("unicode_escape")
        elif opt in ("-i", "--input"):
            # input and dest are the same unless dest is defined with a -d or --dest options
            inputPath = arg
        elif opt in ("-e", "--encoding"):
            enc = arg

    if os.path.exists(inputPath):
        if os.path.isfile(inputPath):
            process_file(inputPath)
        elif os.path.isdir(inputPath):
            for f in os.listdir(inputPath):
                process_file(os.path.join(inputPath, f))
        else:
            print(f'Cannot process input \"{inputPath}\".')


if __name__ == "__main__":
    main(sys.argv[1:])
