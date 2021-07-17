import os
import numpy as np
import argparse
import re
from datetime import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar

#function to obtain the monday of the week of a day that we use.
def get_monday_of_weekdate(date):
    start_of_week = date - timedelta(days=date.weekday())
    return start_of_week

#function to get a list of the starting days of the weeks contained in our list of weeks.
#Our starting day is Monday.
def get_list_of_starting_dates_weeks(list_dates):
    #get the latest and most recent dates in the
    latest_date,most_recent_date=min(list_dates),max(list_dates)

    #get the monday of the week of the latest date, the week number of the earliest date,
    #and the week number of the latest date.
    earliest_monday = get_monday_of_weekdate(latest_date)
    print (earliest_monday)
    week_number_earliest_date=latest_date.strftime('%U')
    week_number_latest_date=most_recent_date.strftime('%U')

    list_weeks_starting_dates=[]

    #Go throught all the weeks and get the monday of each week
    for week_number in range(int(week_number_earliest_date),int(week_number_latest_date)+1):
        list_weeks_starting_dates.append(earliest_monday)
        earliest_monday = earliest_monday + timedelta(7)

    return list_weeks_starting_dates

#function to get a list of the months in out dataset.
def get_list_of_months(list_dates):
    #get the latest and most recent dates in the
    latest_date,most_recent_date=min(list_dates),max(list_dates)

    #get the monday of the week of the latest date, the week number of the earliest date,
    #and the week number of the latest date.
    latest_month= most_recent_date.strftime("%m")
    earliest_month = latest_date.strftime("%m")

    list_months=[]

    #Go throught all the weeks and get the monday of each week
    for month in range(int(earliest_month),int(latest_month)+1):
        list_months.append(month)

    return list_months

#Funtion to
def printing_dictionary(files_to_group,dictionary):
    #printing statements.
    print('\n')
    print ('There are a total of %i files ' %len(files_to_group))
    for key in dictionary.keys():
        date=str(key)
        print ('There are %i items in the date %s' %(len(dictionary[key]),date))

#Funtion that given a dictionary, creates a txt file with the keys and the
#elements of the list of the values are recorded in the txt.
def save_txt_dictionary(dictionary_items):
    for key in dictionary_items.keys():
        f=open(os.path.join(args.outputdir,str(key)+'.txt'), 'w')
        for element in dictionary_items[key]:
            f.write(element)
            f.write('\n')
        f.close()

#function to separate files by the dates on the file name by the week of these dates.
def separate_files_by_dates_week(args):
    #list all the items in the desirted directory with the desired extension.
    files_to_group=[]
    files_to_group += [str(each) for each in os.listdir(args.filedir) if each.endswith(args.fileextension)]

    #get a list of the dates based on all the files we got.
    dates=[datetime.strptime(re.search(args.dateformatfilename, file).group(),
            args.dateformat).date() for file in files_to_group]

    list_weeks_starting_dates=get_list_of_starting_dates_weeks(dates)

    #dictionary with the keys as the day that stars the week. The idea is to put
    #the instances that belong to that week within the value assigned to the key
    weeks_dictionary={date:[] for date in list_weeks_starting_dates}


    #go through all the items and group them based on the week that they belong
    for file in files_to_group:
        for week in weeks_dictionary.keys():
            week_number=week.strftime('%U')
            file_date=datetime.strptime(re.search(args.dateformatfilename,
                        file).group(),args.dateformat).date()

            if file_date.strftime('%U') == week_number:

                #Whether to use the full path or just the file name
                if args.full_path:
                    filepath=os.path.join(args.filedir,file)
                else:
                    filepath=file

                #save image in the dictionary recording the files in each group.
                weeks_dictionary[week].append(filepath)


    #printing statements.
    printing_dictionary(files_to_group,weeks_dictionary)

    #save the grouped items into a txt in the desired directory
    save_txt_dictionary(weeks_dictionary)

#Function to separe the items by the month of the filename.
def separate_files_by_dates_months(args):
    #list all the items in the desirted directory with the desired extension.
    files_to_group=[]
    files_to_group += [str(each) for each in os.listdir(args.filedir) if each.endswith(args.fileextension)]

    #get a list of the dates based on all the files we got.
    dates=[datetime.strptime(re.search(args.dateformatfilename, file).group(),
            args.dateformat).date() for file in files_to_group]

    list_months=get_list_of_months(dates)

    #dictionary with the keys as the month. The idea is to put
    #the instances that belong to that month within the value assigned to the key
    month_dictionary={str(calendar.month_name[month]):[] for month in list_months}

    #go through all the items and group them based on the week that they belong
    for file in files_to_group:
        for month in list_months:
            file_date=datetime.strptime(re.search(args.dateformatfilename,
                        file).group(),args.dateformat).date()

            if int(file_date.strftime('%m')) == month:

                #Whether to use the full path or just the file name
                if args.full_path:
                    filepath=os.path.join(args.filedir,file)
                else:
                    filepath=file

                #save image in the dictionary recording the files in each group.
                month_dictionary[str(calendar.month_name[month])].append(filepath)

    #printing statements.
    printing_dictionary(files_to_group,month_dictionary)

    #save the grouped items into a txt in the desired directory
    save_txt_dictionary(month_dictionary)


def separate_files_by_weeks_and_titlewords(args):
    #list all the items in the desirted directory with the desired extension.
    files_to_group=[]
    files_to_group += [str(each) for each in os.listdir(args.filedir) if each.endswith(args.fileextension)]

    #get a list of the dates based on all the files we got.
    dates=[datetime.strptime(re.search(args.dateformatfilename, file).group(),
            args.dateformat).date() for file in files_to_group]

    list_weeks_starting_dates=get_list_of_starting_dates_weeks(dates)


    #create a dictionary to store the files that belong to each group.
    dictionary_items={i+'_'+str(date):[] for i in args.items_look for date in list_weeks_starting_dates}


    #go through all the items and group them based on the week that they belong
    for file in files_to_group:
        for week in list_weeks_starting_dates:
            for word_to_group in args.items_look:
                if word_to_group in file:
                    week_number=int(week.strftime('%U'))
                    file_date=datetime.strptime(re.search(args.dateformatfilename,
                                file).group(),args.dateformat).date()

                    if int(file_date.strftime('%U')) == week_number:

                        #Whether to use the full path or just the file name
                        if args.full_path:
                            filepath=os.path.join(args.filedir,file)
                        else:
                            filepath=file

                        #save image in the dictionary recording the files in each group.
                        dictionary_items[word_to_group+'_'+str(week)].append(filepath)
                else:
                    continue

    printing_dictionary(files_to_group,dictionary_items)


    #save the grouped items into a txt in the desired directory
    save_txt_dictionary(dictionary_items)

def separate_files_by_months_and_titlewords(args):
    #list all the items in the desirted directory with the desired extension.
    files_to_group=[]
    files_to_group += [str(each) for each in os.listdir(args.filedir) if each.endswith(args.fileextension)]

    #get a list of the dates based on all the files we got.
    dates=[datetime.strptime(re.search(args.dateformatfilename, file).group(),
            args.dateformat).date() for file in files_to_group]

    list_months=get_list_of_months(dates)


    #create a dictionary to store the files that belong to each group.
    dictionary_items={i+'_'+str(calendar.month_name[month]):[] for i in args.items_look for month in list_months}


    #go through all the items and group them based on the week that they belong
    for file in files_to_group:
        for month in list_months:
            for word_to_group in args.items_look:
                if word_to_group in file:

                    file_date=datetime.strptime(re.search(args.dateformatfilename,
                                file).group(),args.dateformat).date()

                    if int(file_date.strftime('%m')) == month:

                        #Whether to use the full path or just the file name
                        if args.full_path:
                            filepath=os.path.join(args.filedir,file)
                        else:
                            filepath=file

                        #save image in the dictionary recording the files in each group.
                        dictionary_items[word_to_group+'_'+str(calendar.month_name[month])].append(filepath)
                else:
                    continue

    printing_dictionary(files_to_group,dictionary_items)


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

    parser.add_argument('--dateformatfilename', type=str, default='\d{2}_\d{2}_\d{4}',
                        help='regular expression format of the dates in the file')

    parser.add_argument('--dateformat', type=str, default='%d_%m_%Y',
                        help='date format of the dates in the file name')

    parser.add_argument('--monthgrouping', action='store_true',
                        help='use the command to group the items by month as well')

    parser.add_argument('--week_and_item_grouping', action='store_true',
                        help='Use it to group your files based on the items and weeks')

    parser.add_argument('--month_and_item_grouping',action='store_true',
                        help='Use it to group your files based on the items and months')

    args=parser.parse_args()

    separate_files_by_dates_week(args)

    if args.monthgrouping:
        separate_files_by_dates_months(args)

    if args.week_and_item_grouping:
        separate_files_by_weeks_and_titlewords(args)

    if args.month_and_item_grouping:
        separate_files_by_months_and_titlewords(args)
