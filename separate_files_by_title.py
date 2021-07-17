import os
import numpy as np
import argparse


#Funtion that given a dictionary, creates a txt file with the keys and the
#elements of the list of the values are recorded in the txt.
def save_txt_dictionary(dictionary_items):
    for key in dictionary_items.keys():
        f=open(os.path.join(args.outputdir,str(key)+'.txt'), 'w')
        for element in dictionary_items[key]:
            f.write(element)
            f.write('\n')
        f.close()

#function to group item by a word in their names
def separate_files_by_name(args):
    #list all the items in the desirted directory with the desired extension.
    files_to_group=[]
    files_to_group += [str(each) for each in os.listdir(args.filedir) if each.endswith(args.fileextension)]

    #create a dictionary to store the files that belong to each group.
    dictionary_items={i:[] for i in args.items_look}

    #go through all the items and group them based on wether contain the word
    #we are looking for.
    for file in files_to_group:
        for word_to_group in args.items_look:
            if word_to_group in file:

                #Whether to use the full path or just the file name
                if args.full_path:
                    filepath=os.path.join(args.filedir,file)
                else:
                    filepath=file

                #save image in the dictionary recording the files in each group.
                dictionary_items[word_to_group].append(filepath)


    #printing statements
    print ('There are a total of %i files ' %len(files_to_group))
    for key in dictionary_items.keys():
        print ('There are %i items in the group %s' %(len(dictionary_items[key]),key))

    #TODO: write down a table indicating the items in each group and save it.

    #save the grouped items into a txt in the desired directory
    save_txt_dictionary(dictionary_items)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--items_look',nargs='+',type=str, default=['near30','bbro'],
                        help='Here write the series of elements in the title that you want to use as a filter')
    parser.add_argument('--outputdir', type=str, default='./',
                        help='directory to save the new list of elements')
    parser.add_argument('--filedir', type=str, default='./',
                        help='directory that contains the files we want to separate')
    parser.add_argument('--fileextension',type=str,default='.txt',
                        help='extension of the files that we want to scan')
    parser.add_argument('--full_path',action='store_true',
                        help='Use to save the full path of the files in each group')
    args=parser.parse_args()

    #run the function that does all the magic :-)
    separate_files_by_name(args)
