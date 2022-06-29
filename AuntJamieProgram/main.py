import pandas as pd
from pandasql import sqldf
import sys
import os
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
import shutil
from datetime import date

working_dataset = pd.read_csv("./databases/default.csv")
documents_dataset = pd.read_csv("./databases/documents_manager.csv")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def open_file_picker():
    root = tk.Tk()
    root.withdraw()

    return filedialog.askopenfilenames()

def operation_loop():
    global working_dataset, documents_dataset
    COLUMNS= ["ID", "CLIENT_NAME", "BILLING/MAILING ADDRESS", "CONTACT_INFO", "PROJECT_ADDRESS", "PROJECT_DESCRIPTION"]
    
    print("---------------------------------------------------------------------------------------------")
    print()
    option = input("What would you like to do? (insert, edit, print, search, upload, file_search, doc_print, quit): ")
    if option == 'insert':
        print("WE ARE GOING TO ADD A NEW ENTRY PLEASE SPECIFY THE INFORMATION PROMPTED, IF NOT AVAILABLE, YOU CAN SIMPLY PRESS ENTER:")
        values = {"ID": None, "CLIENT_NAME": None, "BILLING/MAILING ADDRESS": None, "CONTACT_INFO": None, "PROJECT_ADDRESS": None, "PROJECT_DESCRIPTION": None}
        
        # Check the input of ID outside of general loop
        ID_SUCCESS = False
        while not ID_SUCCESS:
            ID_VALUE = input("ID: ")
            try:
                ID_VALUE = int(ID_VALUE)
                values["ID"] = ID_VALUE
            except:
                print(f"SORRY, TRY AGAIN! {ID_VALUE} is not an INTEGER")
                continue
        
            if ID_VALUE in working_dataset["ID"].tolist():
                print(f"SORRY, {ID_VALUE} is not unique! THIS can cause issues later")
                continue
        
            ID_SUCCESS = True
            
        for i in COLUMNS[1:]:
            value = input(f"{i}: ")
            if value == "":
                value = None
                
            values[i] = value
        
        # Make Corresponding Folder
        if not os.path.isdir(os.path.join('.', str(ID_VALUE))):
            os.mkdir(os.path.join('.', str(ID_VALUE)))
    
        # append row to dataset
        working_dataset = working_dataset.append(values, ignore_index=True)
        
            
    elif option == 'edit':
        ID_SUCCESS = False
        REQUESTED_ID = None
        while not ID_SUCCESS:
            REQUESTED_ID = input("PLEASE ENTER THE ID YOU WISH TO EDIT: ")
            try:
                REQUESTED_ID = int(REQUESTED_ID)
            except:
                print(f"SORRY, TRY AGAIN! {REQUESTED_ID} is not an INTEGER")
                continue
            
            if REQUESTED_ID not in working_dataset["ID"].tolist():
                print(f"SORRY, {REQUESTED_ID} is not in this database!")
                continue
            
            ID_SUCCESS = True
        
        EDIT_COLUMN = input(f"PLEASE ENTER A CORRESPONDING COLUMN {COLUMNS[1:]} or \"quit\" TO EXIT: ")
        while EDIT_COLUMN != "quit":
            if EDIT_COLUMN not in COLUMNS[1:]:
                print(f"INVALID COMMAND: {EDIT_COLUMN} is not in {COLUMNS}")
            else:
                COLUMN_VALUE = input(f"NOW INPUT THE VALUE YOU WISH TO CHANGE THE {EDIT_COLUMN} TO: ")
                working_dataset.loc[working_dataset['ID'] == REQUESTED_ID, EDIT_COLUMN] = COLUMN_VALUE
            EDIT_COLUMN = input(f"PLEASE ENTER A CORRESPONDING COLUMN {COLUMNS[1:]} or \"quit\" TO EXIT: ")
            
    elif option == "doc_print":
        print(documents_dataset)   
        
    elif 'print' in option:
        print(working_dataset)
    
    elif option == 'search':
        SEARCH_COLUMN = input(f"PLEASE ENTER A SEARCH COLUMN {COLUMNS} or \"cancel\" TO EXIT: ")
        while SEARCH_COLUMN != "cancel":
            if SEARCH_COLUMN not in COLUMNS:
                print(f"INVALID COMMAND: {SEARCH_COLUMN} is not in {COLUMNS}")
            elif SEARCH_COLUMN == "ID":
                
                SUCCESS = False
                while not SUCCESS:
                    COLUMN_VALUE = input(f"NOW INPUT THE ID YOU WANT: ")
                    try:
                        COLUMN_VALUE = int(COLUMN_VALUE)
                    except:
                        print(f"SORRY, TRY AGAIN! {COLUMN_VALUE} is not an INTEGER")
                        continue
                    
                    if COLUMN_VALUE not in working_dataset["ID"].tolist():
                        print(f"SORRY, {COLUMN_VALUE} is not in this database!")
                        continue
                
                    SUCCESS = True

                print(working_dataset[working_dataset['ID'] == COLUMN_VALUE])
            else:
                COLUMN_VALUE = input(f"NOW INPUT THE VALUE YOU WISH TO USE TO SEARCH FOR: ")
                rows_that_match = []
                for row_index, row  in tqdm(working_dataset.iterrows(), desc="SEARCHING~"):
                    if COLUMN_VALUE.lower() in row[SEARCH_COLUMN].lower():
                        rows_that_match.append(row_index)
                print(working_dataset.loc[rows_that_match])
            print()
            SEARCH_COLUMN = input(f"PLEASE ENTER A SEARCH COLUMN {COLUMNS} or \"cancel\" TO EXIT: ")
            

    elif option == 'upload':
        print("A FILE CHOOSER WILL OPEN NOW, CHOOSE THE FILE(S) YOU WOULD LIKE TO UPLOAD!")
        file_paths = open_file_picker()
        COLUMN_VALUE = None
        SUCCESS = False
        while not SUCCESS:
            COLUMN_VALUE = input(f"NOW INPUT THE ID YOU WANT TO UPLOAD THESE DOCUMENTS UNDER: ")
            try:
                COLUMN_VALUE = int(COLUMN_VALUE)
            except:
                print(f"SORRY, TRY AGAIN! {COLUMN_VALUE} is not an INTEGER")
                continue
                    
            if COLUMN_VALUE not in working_dataset["ID"].tolist():
                print(f"SORRY, {COLUMN_VALUE} is not in this database!")
                continue
                
            SUCCESS = True
            
        todays_date = date.today().strftime("%m/%d/%Y")
        for original_file_loc in file_paths:
            print(f"COPYING FILE {original_file_loc} TO PROPER PLACE AND ADDING TO DATABASE!")
            shutil.copyfile(original_file_loc, os.path.join('.', str(COLUMN_VALUE), original_file_loc.split("/")[-1]))
            documents_dataset = documents_dataset.append({"ID": int(COLUMN_VALUE), "DOCUMENT": original_file_loc.split("/")[-1], "DATE_ADDED": todays_date}, ignore_index=True)
            
    elif option == "file_search":
        SEARCH_COLUMN = input(f"PLEASE ENTER A SEARCH COLUMN {COLUMNS} OR \"cancel\" TO EXIT: ")
        while SEARCH_COLUMN != "cancel":
            if SEARCH_COLUMN not in COLUMNS:
                print(f"INVALID COMMAND: {SEARCH_COLUMN} is not in {COLUMNS}")
            elif SEARCH_COLUMN == "ID":
                
                SUCCESS = False
                while not SUCCESS:
                    COLUMN_VALUE = input(f"NOW INPUT THE ID YOU WANT: ")
                    try:
                        COLUMN_VALUE = int(COLUMN_VALUE)
                    except:
                        print(f"SORRY, TRY AGAIN! {COLUMN_VALUE} is not an INTEGER")
                        continue
                    
                    if COLUMN_VALUE not in working_dataset["ID"].tolist():
                        print(f"SORRY, {COLUMN_VALUE} is not in this database!")
                        continue
                
                    SUCCESS = True
                    
                temp_df = working_dataset[working_dataset['ID'] == COLUMN_VALUE].merge(documents_dataset, left_on='ID', right_on='ID')
                #document_list = temp_df['DOCUMENT']
                print(temp_df)
                print()
                fs_option = input("TYPE THE DOCUMENT YOU WOULD LIKE TO OPEN OR TYPE \'cancel\' TO QUIT: ")
                while fs_option.lower() != 'cancel':
                    if fs_option.lower() == 'cancel':
                        break
                    else:
                        for _, row in temp_df.iterrows():
                            if fs_option == row['DOCUMENT']:
                                file_loc = os.path.join('.', str(row['ID']), row['DOCUMENT'])
                                os.system(f"start {file_loc}")
                    fs_option = input("TYPE THE DOCUMENT YOU WOULD LIKE TO OPEN OR TYPE \'cancel\' TO QUIT: ")
                print()
            else:
                COLUMN_VALUE = input(f"NOW INPUT THE VALUE YOU WISH TO USE TO SEARCH FOR: ")
                rows_that_match = []
                for row_index, row  in tqdm(working_dataset.iterrows(), desc="SEARCHING~"):
                    if COLUMN_VALUE.lower() in row[SEARCH_COLUMN].lower():
                        rows_that_match.append(row_index)
                        
                temp_df = working_dataset.loc[rows_that_match].merge(documents_dataset, left_on='ID', right_on='ID')
                print(temp_df)
                print()
                while fs_option.lower() != 'cancel':
                    if fs_option.lower() == 'cancel':
                        break
                    else:
                        for _, row in temp_df.iterrows():
                            if fs_option == row['DOCUMENT']:
                                file_loc = os.path.join('.', str(row['ID']), row['DOCUMENT'])
                                os.system(f"start {file_loc}")
                    fs_option = input("TYPE THE DOCUMENT YOU WOULD LIKE TO OPEN OR TYPE \'cancel\' TO QUIT: ")
                print()
            print()
            SEARCH_COLUMN = input(f"PLEASE ENTER A SEARCH COLUMN {COLUMNS} OR \"cancel\" TO EXIT: ")
            
     
            
    elif option == "quit":
        working_dataset.to_csv('./databases/default.csv', index=False)
        documents_dataset.to_csv('./databases/documents_manager.csv', index=False)
        sys.exit(0)
        
    
    else:
        print("FSORRY THAT IS A VALID COMMAND!")
    
    working_dataset.to_csv('./databases/default.csv', index=False)
    documents_dataset.to_csv('./databases/documents_manager.csv', index=False)
    print()

if __name__ == "__main__":

    
    if len(sys.argv) > 1:
        
        if sys.argv[1] == 'create_dataset':
            new_dataset_dict = {}
            for i in ["ID", "CLIENT_NAME", "BILLING/MAILING ADDRESS", "CONTACT_INFO", "PROJECT_ADDRESS", "PROJECT_DESCRIPTION"]:
                new_dataset_dict[i] = []
                
            df = pd.DataFrame.from_dict(new_dataset_dict)
            df.to_csv("./databases/default.csv", index=False)
            
            new_dataset_dict = {}
            for i in ["ID", "DOCUMENTS"]:
                new_dataset_dict[i] = []
                
            df = pd.DataFrame.from_dict(new_dataset_dict)
            df.to_csv("./databases/default.csv", index=False)
            
        if sys.argv[1] == "create_folders":
            temp_df = pd.read_csv('./databases/default.csv')
            for index, row in temp_df.iterrows():
                if os.path.isdir(os.path.join('.', str(row['ID']))):
                    continue
                else:
                    os.mkdir(os.path.join('.', str(row['ID'])))

    while(True):
        operation_loop()