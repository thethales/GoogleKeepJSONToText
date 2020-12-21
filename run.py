import os
import json
import sys
import time




def usecTimeStampToText(timeStamp):
    try:
        
        dt_object = time.strftime("%D %H:%M", time.localtime(int(timeStamp)))
        
        return 'dt_object'
    except: 
        return ''
    


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
            f.write("\n")

            #Google Keep note is of the type plain text
            if 'textContent' in data:
                f.write(data['textContent'])

            #Google Keep note is of the type list text
            if 'listContent' in data:
                f.write("\n")
                for item in data['listContent']:
                    f.write(" - " + item['text'])
                    f.write("\n")

            #Footer
            f.write("\n")
            f.write("---")
            f.write("\n")

            #Datetime
            date_time = usecTimeStampToText(data['userEditedTimestampUsec'])
            if date_time != '':
                f.write('Last edited in ' + date_time)

            #Labels -> Are converted to hashtags
            if 'labels' in data:
                f.write("\n")
                for label in data['labels']:
                    f.write('#' + label['name'])
            
            f.close()
        return True

    except Exception as e:
        print("Unable to process file: " , file_name, "Error: ", str(e)) 
        return False




def main():
    root = os.getcwd()

    if os.path.isdir(os.path.join(root,'Keep')):
        root = os.path.join(root,'Keep')
    
    output_folder = os.path.join(root,'converted')
    result_metrics = {
        'processed_files': 0,
        'skipped_files':0
    }


    createOutputFolder(output_folder)

    print('Processing files...')

    google_keep_files = os.listdir(root)
   
    for dirs in google_keep_files:
        if '.json' in dirs:
            if convertFile(os.path.join(root,dirs),output_folder):
                result_metrics['processed_files'] += 1
            else:
                result_metrics['skipped_files'] += 1

    print('Done.', '\n')
    print('Total files: ', result_metrics['processed_files'] + result_metrics['skipped_files'], '\n' )
    print('Processed files: ', result_metrics['processed_files'],  '\n' )
    print('Skipped files: ', result_metrics['skipped_files'],  '\n' )


if __name__ == "__main__":
    main()