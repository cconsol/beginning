#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 16:14:43 2020

@author: carla
"""
from lexical_diversity import lex_div as ld
import glob
import math
# import spacy
# from spacy_spanish_lemmatizer import SpacyCustomLemmatizer



def splitter(input_string): #presumes that the list is tab-delimitted
    output_list = []
    #insert code
    for x in input_string.split("\n")[1:]: #iterate through sample string split by "\n", skip header row
        cols = x.split("\t") #split the item by "\t"
        word = cols[0] #the first item will be the word
        freq = cols[1] #the second will be the frequency value
        output_list.append([word,freq]) #append the [word, freq] list to the output list

    return(output_list)

def freq_dicter(input_list):
    output_dict = {}
    #insert code here
    for x in input_list: #iterate through list
        word = x[0] #word is the first item
        freq = float(x[1]) #frequency is second item (convert to float using float())
        output_dict[word] = freq #assign key:value pair

    return(output_dict)

def file_freq_dicter(filename):
    #out_dict = {} #if you use the previously defined function freq_dicter() this is not necessary
    spreadsheet = open(filename, errors = 'ignore').read() #open and read the file here
    split_ss = splitter(spreadsheet)#split the string into rows
    out_dict = freq_dicter(split_ss)#iterate through the rows and assign the word as the key and the frequency as the value

    return(out_dict)


CREA_freq = file_freq_dicter("CREA_freq_2020-12-04.txt")


def safe_divide(numerator,denominator): #this function has two arguments
    if denominator == 0: #if the denominator is 0
        output = 0 #the the output is 0
    else: #otherwise
        output = numerator/denominator #the output is the numerator divided by the denominator

    return(output) #return output


def word_counter(low): #list of words
    nwords = len(low)
    return(nwords)

def frequency_count(tok_text,freq_dict):
    freq_sum = 0
    word_sum = 0
    for x in tok_text:
        if x in freq_dict: #if the word is in the frequency dictionary
            freq_sum += math.log(freq_dict[x]) #add the (logged) frequency value to the freq_sum counter #carla_comment: this line keeps throwing this error: File "/Users/carla/Desktop/Corpus/Final_Project /final.py", line 65, in frequency_count freq_sum += math.log(freq_dict[x]) #add the (logged) frequency value to the freq_sum counter TypeError: string indices must be integers
            word_sum += 1 #add one to the word_sum counter
        else:
            continue #if the word isn't in the frequency dictionary, we will ignore it in our index calculation

    return(safe_divide(freq_sum,word_sum)) #return average (logged) frequency score for words in the text


def tokenize(input_string):
    tokenized = [] #empty list that will be returned

    #this is a sample (but incomplete!) list of punctuation characters
    punct_list = [".", "?","!",",","'"]

    #this is a sample (but potentially incomplete) list of items to replace with spaces
    replace_list = ["\n","\t"]

    #This is a sample (but potentially incomplete) list if items to ignore
    ignore_list = [""]

    #iterate through the punctuation list and replace each item with a space + the item
    for x in punct_list:
        input_string = input_string.replace(x," " + x)

    #iterate through the replace list and replace it with a space
    for x in replace_list:
        input_string = input_string.replace(x," ")

    #our examples will be in English, so for now we will lower them
    #this is, of course optional
    input_string = input_string.lower()

    #then we split the string into a list
    input_list = input_string.split(" ")

    #finally, we ignore unwanted items
    for x in input_list:
        if x not in ignore_list: #if item is not in the ignore list
            tokenized.append(x) #add it to the list "tokenized"

    #Then, we return the list
    return(tokenized)



def text_extractor(text): #text is a string
    meta_d = {}
    lines = text.split("\n")
    text_check = False
    for line in lines:
        if text_check == True and ":" not in line:
            meta_d["Text"] = meta_d["Text"] + line
        items = line.split(": ") #split on ": "
        if len(items) < 2: #check for empty lines
            continue
        meta_d[items[0]] = items[1]
        if items[0] == "Text":
            text_check = True
    return(meta_d)


#process entire files
def CEDEL_Processor(folder,outname): #folder name, name of output file
    outf = open(outname,"w") #create output file
    outf.write("\t".join(["Participant","Placement_test","Task","Age","Proficiency","Nwords","MATTR", "HDD", "MTLD", "Av_Freq", "Stay Abroad", "Medium", "Location", "Resources", "Age of exposure", "Years studying"])) #write header
    filenames = glob.glob(folder + "/*") #get filenames in folder
    
    for filename in filenames: #iterate through filenames
        simple_fname = filename.split("/")[-1] #get last part of filename
        text = open(filename, encoding='utf-8').read() #read file
        text_d = text_extractor(text) #create text dictionary
        text_d["nwords"] = word_counter(text_d["Text"].split(" ")) #calculate number of words
        text_d["tokenized"] = tokenize(text_d["Text"])
       # text_d["lemmatized"] = 
        text_d["av_freq"] = frequency_count(text_d["tokenized"],CREA_freq)
        text_d["MATTR"] = ld.mattr(text_d["tokenized"]) #lexical diversity
        text_d["HDD"] = ld.hdd(text_d["tokenized"]) #lexical diversity
        text_d["MTLD"] = ld.mtld(text_d["tokenized"]) #lexical diversity
        out_line = [simple_fname,text_d["Placement test score (%)"],text_d["Task number"],text_d["Age"],text_d["Proficiency"],str(text_d["nwords"]),str(text_d["MATTR"]),str(text_d["HDD"]),str(text_d["MTLD"]),str(text_d["av_freq"]),text_d["Stay abroad (months)"],text_d["Writting/audio details"],text_d["Where the task was done"],text_d["Resources used"],text_d["Age of exposure to Spanish"],text_d["Years studying Spanish"]] #create line for output, make sure to turn any numbers to strings
        outf.write("\n" + "\t".join(out_line)) #write line
    
    outf.flush() #flush buffer
    outf.close() #close_file


    
CEDEL_Processor("cedel","results.txt")


# nlp = spacy.load("es")
# lemmatizer = SpacyCustomLemmatizer()
# nlp.add_pipe(lemmatizer, name="lemmatizer", after="tagger")
# for token in nlp(): #how do you load files and interate through them with Spacey? Spacey feels like advanced Egyptian hieroglyphics 
#     return(token.lemma_)






