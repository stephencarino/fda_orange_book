import csv
import json
import os
import sys
import getopt
import pathlib

path = ''
dest = ''

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf,delimiter='~') 

        for row in csvReader: 
            jsonArray.append(row)
  
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

def find_files(filePath, fileDest):
   if os.path.exists(filePath):
      for f in os.listdir(filePath):
         fileExtension = pathlib.Path(f).suffix  
         fileName = pathlib.Path(f).stem     
         fullPath = os.path.join(filePath, fileName + fileExtension)
         # checking if it is a file and potentially valid for conversion
         if os.path.isfile(fullPath) and fileExtension in ('.csv','.txt','.prn'):
            #print('JSON:',os.path.join(fileDest,fileName+'.json'))
            csv_to_json(fullPath,os.path.join(fileDest,fileName+'.json'))

def main(argv):
   '''
   csv-to-json.py -i <path> -d <dest>

   JSON files are created in the same folder if -d is omitted 
   '''
   global path, dest
   opts, args = getopt.getopt(argv,"hi:d:",["path=","dest="])
   for opt, arg in opts:
      if opt == '-h':
         print (main.__doc__)
         sys.exit()
      elif opt in ("-i", "--path"):
         path = arg
         dest = arg
      elif opt in ("-d", "--dest"):
         dest = arg

   
if __name__ == "__main__":
   main(sys.argv[1:])
   find_files(path, dest)

  


