# This code is intended to be called from a webpage submission (maybe via php)
#
# The webpage submission should capture desired search year, name, email, orcid, affiliation, search terms, etc that include things like this example:
# 2023, James Chambers, jjchambe@umass.edu, 0000-0003-3883-8215, University of Massachusetts, Amherst, confocal, nikon, a1r, Nikon Center of Excellence, IALS, ga3, strom, MLSC, spinning disk, SCR_021148, jjchambe@umass.edu, James Chambers, University of Massachusetts, Amherst
# 
# The webpage submission also accepts (expects) a csv file containing a list of names of users of the facility (and possibly their faculty advisors)
#
# This then does two rounds of searching of the data accumulated by 1-TheScraper:
# -it matches authors from the citations to the csv file
# -it matches keywords from the input data to the plain text manuscripts
#
# This then is weignhted in score and ranked in output
# 
##########
##  To do
##  so much

import csv
import os
import re
import pandas as pd

#just doing some csv reading
def read_words_from_file(file_name):
    words = []
    with open(file_name, 'r') as file:
        for line in file:
            words.extend(line.split(", "))
    return words

#just grabbing the article number into a variable
def extract_second_number_group(s):
    pattern = r'\d+'
    matches = re.findall(pattern, s)
    if len(matches) >= 2:
        return matches[1]
    else:
        return None  # Return None if there is no second group
    
#count up the keyword matches
def find_keywords_in_file(file_path, keywords):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            results = {keyword: text.count(keyword) for keyword in keywords}
            return results
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#match manuscript authors to the citations from pubmed
def find_auths_in_line(line, auths):
    try:
        results = {auth: line.count(auth) for auth in auths}
        return results
    except FileNotFoundError:
        print(f"Error: The file '{auth_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#these are hardcoded because i didn't get it onto a website yet for php execution
term_file = "/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/www/data.txt"
term_list_raw = read_words_from_file(term_file)
auth_file = "/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/www/users.csv"
auth_list_raw = read_words_from_file(auth_file)
words_2_remove = ['2020', '2021', '2022', '2023', '2024']
term_list = [word for word in term_list_raw if word not in words_2_remove]
auth_list_cleaned = [word for word in auth_list_raw if word not in words_2_remove]
auth_list_all = [line.strip() for line in auth_list_cleaned]
auth_list = list(set(auth_list_all))
last_names = [item.split()[-1] for item in auth_list]
syear = 2023

#for each manuscript txt file, grab starting number in order to output the citation from the master annual file from one directory up.
annualsum = f'CY{syear}_annual.txt'
annualdir = f'CY{syear}_text_results'
outputs = []
authoutputs = []
for filename in os.listdir(annualdir):
    file_path = os.path.join(annualdir, filename)
    if os.path.isfile(file_path):
        articlenum = extract_second_number_group(file_path)
        termscore = 0 #DONE!! FIND TERM LIST MATCHES
        termresults = find_keywords_in_file(file_path, term_list)       
        if termresults:
            for keyword, termcount in termresults.items():
                termscore = termscore + termcount#        authscore = 0
            termweight = 100
            termscore = termscore * termweight
            if termscore>100:
                outputs.append(f"{articlenum}, {termscore}")
                sorted_outs = sorted(outputs, key=lambda x: x[:3])
            else:
                bob = 1
with open(annualsum, 'r') as file:
    for line in file:
        #get article numb from current line - authline
        line = line.strip()
        fields = line.split('|')
        if fields:
            authline = fields[0].strip()
        authscore = 0
        authresults = find_auths_in_line(line, last_names)
        for auth, authcount in authresults.items():
            authscore = authscore + authcount
        if authscore>1:
            authoutputs.append(f"{authline}, {authscore}")
            sorted_authouts = sorted(authoutputs, key=lambda x: x[:3])
        else:
            bob = 1

#the rest of this code is awful because it is opening and closing the same csv file over and over to make minor modificaitons...bad coder, Jim.
with open("tosort_data.csv", 'w') as f:
    for row in sorted_outs:
        print(row, file=f)
with open('tosort_data.csv', 'r') as infile:
    reader = csv.reader(infile)
    data = list(reader)
data.sort(key=lambda row: int(row[0]), reverse=True)
with open('sorted_data.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)

with open("atosort_data.csv", 'w') as f:
    for row in sorted_authouts:
        print(row, file=f)
with open('atosort_data.csv', 'r') as infile:
    reader = csv.reader(infile)
    data = list(reader)
data.sort(key=lambda row: int(row[0]), reverse=True)
with open('asorted_data.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)

df1column_names = ['id', 'term']
df2column_names = ['id', 'auth']
df1 = pd.read_csv('sorted_data.csv', header=None)
df2 = pd.read_csv('asorted_data.csv', header=None)
df1.columns = df1column_names
df1.to_csv('termout.csv', index=False)
df2.columns = df2column_names
df2.to_csv('authout.csv', index=False)
df2 = pd.read_csv('termout.csv')
df1 = pd.read_csv('authout.csv')

# Merge the DataFrames on the 'id' column
merged_df = pd.merge(df1, df2, on='id')
merged_df.to_csv('merged_file.csv', index=False)

# remove the old csv files
fp1 = '/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/asorted_data.csv'
fp2 = '/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/atosort_data.csv'
fp3 = '/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/authout.csv'
fp4 = '/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/sorted_data.csv'
fp5 = '/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/termout.csv'
fp6 = '/Users/jameschambers/Library/CloudStorage/Dropbox/LMF/pub/pub/tosort_data.csv'
if os.path.isfile(fp1):
    os.remove(fp1)
if os.path.isfile(fp2):
    os.remove(fp2)
if os.path.isfile(fp3):
    os.remove(fp3)
if os.path.isfile(fp4):
    os.remove(fp4)
if os.path.isfile(fp5):
    os.remove(fp5)
if os.path.isfile(fp6):
    os.remove(fp6)

#  add col2 and 3 or merged_file.csv and then sort by result
df = pd.read_csv('merged_file.csv')
if df.shape[1] >= 3:
    df['sum'] = df.iloc[:, 1] + df.iloc[:, 2]
    df.to_csv('merged_file.csv', index=False)
else:
    print("The DataFrame does not have enough columns.")

column_to_move = 'sum'
new_order = [column_to_move] + [col for col in df.columns if col != column_to_move]
df = df[new_order]
df.to_csv('merged_file.csv', index=False)

# paste in the doi link and rest of citation into the line
df3column_names = ['id', 'quality', 'doi']
df3 = pd.read_csv(annualsum, header=None, delimiter='|')
df3.columns = df3column_names
#df3.to_csv('tempdoi.csv', index=False)

merged_df = pd.merge(df, df3, on='id')
merged_df.to_csv('merged_file.csv', index=False)

df = pd.read_csv('merged_file.csv')
df_sorted = df.sort_values(by='sum', ascending=False)
df_sorted.to_csv("merged_file.csv", index=False)


# don't output if no matches for author or for terms
