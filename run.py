import os
import json
import sys

from datetime import datetime



def usecTimeStampToText(timeStamp:int):
    try:
        dt_object = datetime.fromtimestamp(timestamp)
    except: 
        dt_object = ''
    return str(dt_object)


def createOutputFolder(output_folder:str):
    try:
        if(not os.path.isdir(output_folder)):
            os.mkdir(output_folder)
    except OSError:
        print ("Creation of the output directory %s failed" % output_folder, 'Unable to proceed')
        sys.exit()
    else:
        print ("Successfully created the output directory %s " % output_folder)



def convertFile(file_path:str, output_folder:str):
    file_name = os.path.basename(file_path)
    output_file_path = os.path.join(output_folder,os.path.splitext(file_name)[0]+'.txt')
    
    try:
        with open(file_path) as f:
            data = json.load(f)

            f = open(output_file_path, "w")
            f.write(data['title'])
            f.write("\n")
            f.write('Last edited in ')
            f.write(usecTimeStampToText(data['userEditedTimestampUsec']))
            f.write("\n")
            f.write(data['textContent'])
            f.close()
            
    except Exception as e:
        print("Unable to process file: " , file_name, "Error: ", str(e)) 




def main():
    root = os.getcwd()
    output_folder = os.path.join(root,'converted')


    createOutputFolder(output_folder)

    print('Processing files')

    for dirs in os.listdir(root):
        if '.json' in dirs:
            convertFile(os.path.join(root,dirs),output_folder)

    print('Done. Check the output folder for the processed files: ', output_folder)


if __name__ == "__main__":
    main()