import json
import sys
import getopt
import requests as rq
import time
import os

inputFile = ''
outFile = ''
data = []


def get_pubchem_data(attrib,data):
    unique_list =[]
    
    for item in data:
        ingredients=[]
        #split if multicomponent
        if "; "  in item[attrib]: #format appears to be "CompontentA; ComponentB"
            ingredients = item[attrib].split(';')
        else:
            ingredients.append(item[attrib]) #create a list from a single component

        for ingredient in ingredients:
            ingredient = ingredient.strip()
            # check if exists in unique_list or not
            if ingredient not in unique_list:
                unique_list.append(ingredient)
            
    
    #list_str = ','.join(unique_list)
    
    # search the list in PubChem

    pubchem_data = []

    for item in unique_list:
        
        pubchem_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/' + item + \
                  '/property/'\
                  'IUPACName,'\
                  'MolecularFormula,'\
                  'MolecularWeight,'\
                  'CanonicalSMILES,'\
                  'XLogP,Complexity,'\
                  'AtomStereoCount,'\
                  'BondStereoCount,'\
                  'CovalentUnitCount,'\
                  'FeatureAnionCount3D,'\
                  'FeatureCationCount3D' + \
                  '/JSON'
        try:
            output = rq.get(pubchem_url)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            js_data = json.loads(output.content)
            js_data["Name"] = item
            pubchem_data.append(js_data)
        time.sleep(0.5)

    #write to file
    with open(pubchem_file, "w") as outfile:
        json.dump(pubchem_data, outfile)
    


def crosscheck_pubchem_data():
    pubchem_file = './current-release/pubchem_out.json'
    pubchem_results = './current-release/pubchem_results.json'
    
    data=[]
    # Open JSON file
    iFile = open(pubchem_file)

    # returns JSON object as a dictionary
    pubchem_data = json.load(iFile)

    #check for CID
    for item in pubchem_data:
        i = 1
        try:
            #iterate in case there are multiple search results

            for entry in item["PropertyTable"]["Properties"]:
                mol_data={}
                mol_data["Name"]=item["Name"]
                mol_data["CID"] = entry["CID"]
                mol_data["URL"] = "https://pubchem.ncbi.nlm.nih.gov/compound/" + str(entry["CID"])
                mol_data["AutoFound"] = True #entry was found in name search
                mol_data["Hit"] = i; i+=1
                mol_data["ValidHit"] = True #flag if useable in the analysis
                mol_data["Comments"] =""
                data.append(mol_data)
        except:
            mol_data={}
            mol_data["Name"]=item["Name"]
            mol_data["CID"] = -1
            mol_data["URL"] = ""
            mol_data["AutoFound"] = False
            mol_data["Hit"] = i
            mol_data["ValidHit"] = False #flag if useable in the analysis
            mol_data["Comments"]=""
            data.append(mol_data)
       
    #write to file
    with open(pubchem_results, "w") as oFile:
        json.dump(data, oFile)
            

def clean_pubchem_data():
    pubchem_file = './current-release/pubchem_out.json'
    data = []
    # Open JSON file
    iFile = open(pubchem_file)
    # returns JSON object as a dictionary
    pubchem_data = json.load(iFile)

    #flatten
    for item in pubchem_data:
        for entry in item["PropertyTable"]["Properties"]:
            mol_data = entry
        mol_data["Name"]=item["Name"]
        print(mol_data["Name"])
        
        data.append(mol_data)

        pubchem_data = json.dumps(data)
    
    #print(pubchem_data)
    
    #write to file
    with open(pubchem_file, "w") as oFile:
        json.dump(pubchem_data, oFile)
            
    


def process_file (_inputFile, _outFile):

    global data
    # Opening JSON file
    iFile = open(_inputFile)
    # returns JSON object as a dictionary
    data = json.load(iFile)

    # split 'DF; Route'
    for item in data:
        if ';' in (item['DF;Route']):
            DF, Route = item['DF;Route'].split(';')
            item['DF'] = DF
            item['Route'] = Route

    #write to file
    with open(_outFile, "w") as oFile:
        json.dump(data, oFile)
            

        

def main(argv):
    '''
    products.py -i <inputFile> -o <outFile>

    File is copied in the same folder if -o is omitted 
    '''
    global inputFile, outFile
    opts, args = getopt.getopt(argv,"hi:d:",["inputFile=","outFile="])
    for opt, arg in opts:
        if opt == '-h':
            print(main.__doc__)
            #print ('products.py -i <inputFile> -d <outFile>')
            sys.exit()
        elif opt in ("-i", "--inputFile"):
            inputFile = arg
            outFile = arg
        elif opt in ("-o", "--outFile"):
            outFile = arg


if __name__ == '__main__':
    #main(sys.argv[1:])
    #process_file(inputFile, outFile)
    #get_pubchem_data('Ingredient',data)
    #clean_pubchem_data()
    crosscheck_pubchem_data()