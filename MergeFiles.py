#!/usr/bin/env python
import os
import csv
import pandas as pd
os.chdir((input("Enter the full path for the files: ")))

# TODO add a way to automatically import the data from Syncro API for "Installed Apps"

# open up a SentinelOne CSV file and only keep the specified columns
sentinelOne = pd.read_csv((input("Enter the SentinelOne File name: ")), encoding='cp1252')
keep_col = ['Name','Version','Publisher','Installed','Agent name']
newSO = sentinelOne[keep_col]
newSO.to_csv("SentinelOneData.csv", index=False)

# read the SentinelOne csv file with cp1252 encoding
df1 = pd.read_csv("SentinelOneData.csv", encoding='cp1252')

# read Syncro csv file with cp1252 encoding
df2 = pd.read_csv((input("Enter the Syncro File name: ")), encoding='cp1252')

# Function to swap the columns for SentinelOne file
def swap_columns(df1, col2, col3):
    col_list = list(df1.columns)
    x, y = col_list.index(col2), col_list.index(col3)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df1 = df1[col_list]
    return df1

# call the function that swaps the columns of SentinelOne to match the order of Syncro
df1 = swap_columns(df1, 'Version', 'Publisher')

# Merge Syncro columns into SentinelOne columns and then concatenate both files
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


