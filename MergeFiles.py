#!/usr/bin/env python
import os
import csv
import pandas as pd
os.chdir((input("Enter the full path for the files: ")))

# open up a file and only keep the specified columns
file1 = pd.read_csv((input("Enter the File1 name: ")), encoding='cp1252')
keep_col = ['Name','Version','Publisher','Installed','Agent name']
newSO = file1[keep_col]
newSO.to_csv("File1Data.csv", index=False)

# read the SentinelOne csv file with cp1252 encoding
df1 = pd.read_csv("File1Data.csv", encoding='cp1252')

# read Syncro csv file with cp1252 encoding
df2 = pd.read_csv((input("Enter the File2 name: ")), encoding='cp1252')

# Function to swap the columns for file1
def swap_columns(df1, col2, col3):
    col_list = list(df1.columns)
    x, y = col_list.index(col2), col_list.index(col3)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df1 = df1[col_list]
    return df1

# call the function that swaps the columns of SentinelOne to match the order of file2
df1 = swap_columns(df1, 'Version', 'Publisher')

# Merge file2 columns into file1 columns and then concatenate both files
# After concatening the files, delete duplicate entries based on the Name and Version columns, keep the last known entry
df2.columns = df1.columns
combined = pd.concat([df1, df2], ignore_index=True, sort=False) \
    .drop_duplicates(['Name', 'Version'], keep='last')

# write the concatenated dataframe to a new csv file with cp1252 encoding and no headers.
combined.to_csv("concatenated_file.csv", encoding='cp1252', index=False, header=0)

# Replace unwanted characters or groups of characters.
sanitize = open("concatenated_file.csv", "r")
sanitize = ''.join([i for i in sanitize]) \
    .replace("&lt;", "<") \
    .replace("&gt;", ">") \
    .replace("&lt;", "<") \
    .replace("Â", "") \
    .replace("„", "") \
    .replace("amp;", "") \
    .replace("®", "") \
    .replace("™", "") \
    .replace("¢", "") \
    .replace("\\", " ") \
    .replace("  ", " ")

# output sanitized file into a new csv file.
x = open("SanitizedCombo.csv", "w")
x.writelines(sanitize)
x.close()


