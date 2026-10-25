#!/usr/bin/env python
# coding: utf-8

# ##### D. Tom 11/2023
# # <center> SynoSearcher: Article and Web Link Finder</center>
# <b>Task: </b>*This Python 3 program first collects a set of user-defined words, then uses the Natural Language Toolkit (NLTK) to find their synonyms. Subsequently, it searches for and outputs relevant articles and web links associated with these keywords and their synonyms, providing a comprehensive resource compilation related to the input terms*.

# ### Introduction
# Using a proof of concept, this project boradens the scope of data analysis and web scraping capabilities for additional free, open-source initiatives.  By integrating the Natural Language Toolkit (NLTK) with the Google-Search library, we use the googlesearch-python scraper to efficiently find and display synonyms, enhancing our data processing capabilities.
# 
# The application of proper Data Science methods and techniques in this project allows for efficient resource allocation, facilitating the achievement of objectives in a cost-effective and timely manner.  This approach not only streamlines processes but also yields significant economic benefits, such as reduced operational costs and improved data-driven decision-making.
# 
# <b>Note: Always verify the use case and comply with any applicable terms of service before using this project.</b>
# 
# - <b>Understand Service Limitations:</b> Be aware of the limitations and restrictions of the services utlized, as these can influence the project's functionality and legal compliance.
# 
# - <b>Data Privacy and Ethics:</b> Ensure adherence to privacy laws and ethical standards in data scraping and analysis, particularly when handling sensitive or proprietary information.
# 
# - <b>Regular Updates and Maintenance:</b> Maintain the software with regular updates to integrate the latest NLTK and Google API advancements and to address any security vulnerabilities.
# 
# - <b>Scalability and Performance:</b>Assess the scalability of the project, especially for large-scale data analysis, ensuring that the infrastructure is capable of handling increased data loads and processing demands.
# 
# - <b>Emphasize Accuracy and Reliability:</b> Focus on the accuracy and reliability of data obtained through scraping, as this is critical for meaningful and valid analysis.
# 
# - <b>Promote Collaboration and Knowledge Sharing:</b> Highlight the project's potential for collaboration within open-source communities, fostering innovation and collective learning.
#     
# - <b>User-Friendly Design:</b> If applicable, mention efforts to make the program accessible and easy to use, even for individuals with limited technical background in data science and web scraping.
#     
# This comprehensive approach ensures that the project not only meets its immediate objectives but also adheres to best practices in data science, fostering ethical, legal, and effective data utlization.

# ## Table of Contents
# 
# <div class="alert alert-block alert-info" style="margin-top: 20px">
# 
# 1. [Setting up the Environment](#0)<br>
# 2. [Define Functions](#2)<br>
# 2. [Input Phase](#4)<br>
# 3. [Processing Phase](#6)<br>
# 4. [Output Phase](#8)<br>
# 5. [Main()](#10)<br>
# 6. [Complexity](#12)<br>
# 7. [Conclusion](#14)<br>

# # Setting up the Environment<a id="0"></a>
# The following setup enables the download and import of the NLTK and Google-Search libraries for the project's specific use cases. This environment includes modules that allow obtaining user input, generating a list of words associated with that input, and initiating web scraping. Additional optimization methods can be implemented to add, remove, or omit certain words and modules, tailoring them to the project's specific requirements.

# ##### Upgrade, Install, and Import Dependencies

# In[1]:


# Install dependencies explicitly before running this script:
# python3 -m pip install -r requirements.txt


# In[2]:


# Download the corpora explicitly during setup, not when importing this module:
# python3 -m nltk.downloader omw-1.4 wordnet verbnet


# In[3]:


import re     # for regular expressions on input
import csv    # for csv file inputs
from spellchecker import SpellChecker    # spelling check

import itertools                   # iterate over permutations
from nltk.corpus import wordnet    # Word corpus
from nltk.corpus import verbnet    # Verb corpus
from googlesearch import search    # Google search


# # Define Functions<a id="2"></a>
# 1. <b>Function Prototypes</b>
# 
#     - <b>Input Phase</b>
#         - In this phase, input is obtained and stored for subsequent analysis.  This includes gathering data from various sources and preparing it for processing.
#             - load_words_from_file(file_name)
#             - process_user_input()
#             - check_spelling(words)
#             - split_string(input_string)
#             - get_input_from_user()
#     - <b>Processing Phase</b>
#         - During the processing phase, functions begin processing the input.  This involves performing calculations, data manipulation, and any necessary data transformations to prepare for output.
#             - perform_search(query_list)
#             - get_verbnet_classes(verb)
#             - search_wordnet(word)
#             - get_all_combinations(words_list, synonyms_dict)
#     - <b>Output Phase</b>
#         - The general output phase includes interactions with terminal/emulator I/O streams.  This involves displaying results, exporting data, or generating reports based on the processed input.
#             - print_search_results(search_results)

# ## Input Phase<a id="4"></a>

# In[4]:


# Load csv file for input
def load_words_from_file(file_name):
    words = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.extend(row)
    return ' '.join(words)     # join words into a single string for split_string


# In[5]:


# Obtain words from user
def get_input_from_user():
    return input("Enter your word: ")


# In[6]:


# Seperate words for analysis and processing
def split_string(input_string):
    # Splitting the string by spaces and punctuation
    words = re.findall(r'\b\w+\b', input_string)
    
    # Storing words in a dictionary
    word_dict = {f'word_{i}' : word for i, word in enumerate(words, start=1)}
    
    return words, word_dict


# In[7]:


# Initialize the spell checker
spell = SpellChecker()

# Check the spelling
def check_spelling(words):
    misspelled = spell.unknown(words)
    corrected_words = []
    
    for word in words:
        if word in misspelled:
            # Get the most likely correction
            corrected_word = spell.correction(word) or word
            corrected_words.append(corrected_word)
            if corrected_word != word:
                print(f"Correcting '{word}' to '{corrected_word}' ")
        else:
            corrected_words.append(word)
            
    return corrected_words


# In[8]:


# Function to process user input and prepare input for processing phase
def process_user_input():
    while True:
        user_response = input("Do you have a file of words? (yes or no (y/n)): ").strip().lower()
        if user_response == 'n':
            user_words = get_input_from_user()
            break
        elif user_response == 'y':
            file_name = input("Enter the file name: ")
            user_words = load_words_from_file(file_name)
            break
        else:
            print("Invalid response. Please enter 'y' or 'n'.")

    # words_list, words_dict = split_string(user_words)

    return split_string(user_words)


# ## Processing Phase<a id="6"></a>

# In[9]:


# Obtain all combinations of words and synonyms
def get_all_combinations(words_list, synonyms_dict, max_combinations=100):
    if max_combinations < 1:
        raise ValueError('max_combinations must be positive')
    if not words_list:
        return []
    all_combinations = []
    combination_count = 1
    for word in words_list:
        # Keep the input word even when WordNet has no matching synonyms.
        options = sorted(set([word] + list(synonyms_dict.get(word, []))))
        combination_count *= len(options)
        if combination_count > max_combinations:
            raise ValueError(
                f'Too many search combinations (limit: {max_combinations}). '
                'Use fewer input words or a smaller synonym set.'
            )
        all_combinations.append(options)
    return list(itertools.product(*all_combinations))


# ##### NLTK

# In[10]:


# Noun synonyms
def search_wordnet(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)


# In[11]:


# Verb synonyms
def get_verbnet_classes(verb):
    return verbnet.classids(verb)


# ##### Google Search

# In[12]:


# Function to concatenate words and perform search
def perform_search(query_list):
    results = {}
    for query in query_list:
        # Assuming 'search' is a function you have defined to perform web searches
        results[query] = [url for url in search(query, num_results=1)]
    return results


# ## Output Phase<a id="8"></a>

# In[13]:


# Output search results and urls
def print_search_results(search_results):
    for query, urls in search_results.items():
        # Print the results
        print(f"Search Query: {query}")
        for url in urls:
            print(url)
        print("\n")


# ## Main()<a id="10"></a>

# In[ ]:


def main():
    words_list, _ = process_user_input()
    corrected_words_list = check_spelling(words_list)
    if not corrected_words_list:
        print('No words supplied; no searches were made.')
        return

    # Mapping each word (original or corrected) to its synonyms
    all_words = set(words_list + corrected_words_list)
    synonyms_dict = {word: search_wordnet(word) for word in all_words}
    try:
        all_unique_combinations = get_all_combinations(corrected_words_list, synonyms_dict)
    except ValueError as error:
        print(error)
        return

    unique_search_queries = [' '.join(combination) for combination in all_unique_combinations]
    search_results = perform_search(unique_search_queries)
    print_search_results(search_results)


if __name__ == '__main__':
    main()


# ## Complexity<a id="12"></a>
# For n input words with k_i distinct choices each, the number of combinations is
# the product of k_i. Building all tuples takes O(n * product(k_i)) time and memory;
# the default 100-combination limit is checked before materializing that product.
# Each resulting query may make an external search request. This is multiplicative
# growth in the choices, not logarithmic growth.
