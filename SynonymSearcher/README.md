##### D. Tom 11/2023
# <center> SynoSearcher: Article and Web Link Finder</center>

> Historical learning project. See the [repository overview](../README.md), [contribution guide](../CONTRIBUTING.md), and [licensing notes](../README.md#license). The original notebook walkthrough and sample output are preserved below.

<b>Task: </b>*This Python 3 program first collects a set of user-defined words, then uses the Natural Language Toolkit (NLTK) to find their synonyms. Subsequently, it searches for and outputs relevant articles and web links associated with these keywords and their synonyms, providing a comprehensive resource compilation related to the input terms*.

### Introduction
Using a proof of concept, this project boradens the scope of data analysis and web scraping capabilities for additional free, open-source initiatives.  By integrating the Natural Language Toolkit (NLTK) with the Google-Search library, we harness Google's API to efficiently find and display synonyms, enhancing our data processing capabilities.

The application of proper Data Science methods and techniques in this project allows for efficient resource allocation, facilitating the achievement of objectives in a cost-effective and timely manner.  This approach not only streamlines processes but also yields significant economic benefits, such as reduced operational costs and improved data-driven decision-making.

<b>Note: Always verify the use case and comply with any applicable terms of service before using this project.</b>

- <b>Understand Service Limitations:</b> Be aware of the limitations and restrictions of the services utlized, as these can influence the project's functionality and legal compliance.

- <b>Data Privacy and Ethics:</b> Ensure adherence to privacy laws and ethical standards in data scraping and analysis, particularly when handling sensitive or proprietary information.

- <b>Regular Updates and Maintenance:</b> Maintain the software with regular updates to integrate the latest NLTK and Google API advancements and to address any security vulnerabilities.

- <b>Scalability and Performance:</b>Assess the scalability of the project, especially for large-scale data analysis, ensuring that the infrastructure is capable of handling increased data loads and processing demands.

- <b>Emphasize Accuracy and Reliability:</b> Focus on the accuracy and reliability of data obtained through scraping, as this is critical for meaningful and valid analysis.

- <b>Promote Collaboration and Knowledge Sharing:</b> Highlight the project's potential for collaboration within open-source communities, fostering innovation and collective learning.
    
- <b>User-Friendly Design:</b> If applicable, mention efforts to make the program accessible and easy to use, even for individuals with limited technical background in data science and web scraping.
    
This comprehensive approach ensures that the project not only meets its immediate objectives but also adheres to best practices in data science, fostering ethical, legal, and effective data utlization.

## Table of Contents

<div class="alert alert-block alert-info" style="margin-top: 20px">

1. [Setting up the Environment](#0)<br>
2. [Define Functions](#2)<br>
2. [Input Phase](#4)<br>
3. [Processing Phase](#6)<br>
4. [Output Phase](#8)<br>
5. [Main()](#10)<br>
6. [Complexity](#12)<br>
7. [Conclusion](#14)<br>

# Setting up the Environment<a id="0"></a>
The following setup enables the download and import of the NLTK and Google-Search libraries for the project's specific use cases. This environment includes modules that allow obtaining user input, generating a list of words associated with that input, and initiating web scraping. Additional optimization methods can be implemented to add, remove, or omit certain words and modules, tailoring them to the project's specific requirements.

##### Upgrade, Install, and Import Dependencies


```python
%%capture
import sys
!{sys.executable} -m pip install --upgrade pip
!pip install --upgrade pyspellchecker
!pip install --upgrade googlesearch-python nltk
```


```python
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('verbnet')
```

    [nltk_data] Downloading package omw-1.4 to
    [nltk_data]     C:\Users\User\AppData\Roaming\nltk_data...
    [nltk_data]   Package omw-1.4 is already up-to-date!
    [nltk_data] Downloading package wordnet to
    [nltk_data]     C:\Users\User\AppData\Roaming\nltk_data...
    [nltk_data]   Package wordnet is already up-to-date!
    [nltk_data] Downloading package verbnet to
    [nltk_data]     C:\Users\User\AppData\Roaming\nltk_data...
    [nltk_data]   Package verbnet is already up-to-date!
    




    True




```python
import re     # for regular expressions on input
import csv    # for csv file inputs
from spellchecker import SpellChecker    # spelling check

import itertools                   # iterate over permutations
from nltk.corpus import wordnet    # Word corpus
from nltk.corpus import verbnet    # Verb corpus
from googlesearch import search    # Google search
```

# Define Functions<a id="2"></a>
1. <b>Function Prototypes</b>

    - <b>Input Phase</b>
        - In this phase, input is obtained and stored for subsequent analysis.  This includes gathering data from various sources and preparing it for processing.
            - load_words_from_file(file_name)
            - process_user_input()
            - check_spelling(words)
            - split_string(input_string)
            - get_input_from_user()
    - <b>Processing Phase</b>
        - During the processing phase, functions begin processing the input.  This involves performing calculations, data manipulation, and any necessary data transformations to prepare for output.
            - perform_search(query_list)
            - get_verbnet_classes(verb)
            - search_wordnet(word)
            - get_all_combinations(words_list, synonyms_dict)
    - <b>Output Phase</b>
        - The general output phase includes interactions with terminal/emulator I/O streams.  This involves displaying results, exporting data, or generating reports based on the processed input.
            - print_search_results(search_results)

## Input Phase<a id="4"></a>


```python
# Load csv file for input
def load_words_from_file(file_name):
    words = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.extend(row)
    return ' '.join(words)     # join words into a single string for split_string
```


```python
# Obtain words from user
def get_input_from_user():
    return input("Enter your word: ")
```


```python
# Seperate words for analysis and processing
def split_string(input_string):
    # Splitting the string by spaces and punctuation
    words = re.findall(r'\b\w+\b', input_string)
    
    # Storing words in a dictionary
    word_dict = {f'word_{i}' : word for i, word in enumerate(words, start=1)}
    
    return words, word_dict

```


```python
# Initialize the spell checker
spell = SpellChecker()

# Check the spelling
def check_spelling(words):
    misspelled = spell.unknown(words)
    corrected_words = []
    
    for word in words:
        if word in misspelled:
            # Get the most likely correction
            corrected_word = spell.correction(word)
            corrected_words.append(corrected_word)
            print(f"Correcting '{word}' to '{corrected_word}' ")
        else:
            corrected_words.append(word)
            
    return corrected_words
```


```python
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
```

## Processing Phase<a id="6"></a>


```python
# Obtain all combinations of words and synonyms
def get_all_combinations(words_list, synonyms_dict):
    all_combinations = []
    for word in words_list:
        # Combine original/corrected words with its synonyms
        options = synonyms_dict.get(word, [word])
        all_combinations.append(set(options))
    return list(set(itertools.product(*all_combinations)))
```

##### NLTK


```python
# Noun synonyms
def search_wordnet(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)
```


```python
# Verb synonyms
def get_verbnet_classes(verb):
    return verbnet.classids(verb)
```

##### Google Search


```python
# Function to concatenate words and perform search
def perform_search(query_list):
    results = {}
    for query in query_list:
        # Assuming 'search' is a function you have defined to perform web searches
        results[query] = [url for url in search(query, num_results=1)]
    return results
```

## Output Phase<a id="8"></a>


```python
# Output search results and urls
def print_search_results(search_results):
    for query, urls in search_results.items():
        # Print the results
        print(f"Search Query: {query}")
        for url in urls:
            print(url)
        print("\n")
```

## Main()<a id="10"></a>


```python
# Example:
words_list, words_dict = process_user_input()
corrected_words_list = check_spelling(words_list)

all_words = set(words_list + corrected_words_list)

# Mapping each word (original or corrected) to its synonyms
synonyms_dict = {word: search_wordnet(word) for word in all_words}

# Get all combinations
# all_unique_combinations = get_all_combinations(words_list, synonyms_dict)
all_unique_combinations = get_all_combinations(corrected_words_list, synonyms_dict)

# Combine words into search queries
unique_search_queries = [' '.join(combination) for combination in all_unique_combinations]

# Perform searches for each combined query
search_results = perform_search(unique_search_queries)
print_search_results(search_results)

```

    Do you have a file of words? (yes or no (y/n)): n
    Enter your word: helli
    Correcting 'helli' to 'hell' 
    Search Query: sin
    https://en.wikipedia.org/wiki/Sin
    https://www.merriam-webster.com/dictionary/sin
    https://www.britannica.com/topic/sin-religion
    
    
    Search Query: netherworld
    https://fearworld.com/
    https://fearworld.com/
    
    
    Search Query: hell_on_earth
    https://en.wikipedia.org/wiki/Hell_on_Earth_(Mobb_Deep_album)
    
    
    Search Query: Hades
    https://en.wikipedia.org/wiki/Hades
    https://www.supergiantgames.com/games/hades/
    https://store.steampowered.com/app/1145360/Hades/
    
    
    Search Query: hellhole
    https://www.imdb.com/title/tt19724142/
    https://en.wikipedia.org/wiki/Hellhole_(2022_film)
    
    
    Search Query: infernal_region
    https://www.vocabulary.com/dictionary/infernal%20region
    https://www.thefreedictionary.com/infernal+region
    
    
    Search Query: Hell
    https://en.wikipedia.org/wiki/Hell_in_Christianity
    
    
    Search Query: inferno
    https://www.imdb.com/title/tt3062096/
    https://en.wikipedia.org/wiki/Inferno_(2016_film)
    
    
    Search Query: the_pits
    https://www.merriam-webster.com/dictionary/the%20pits
    https://www.meetatthepit.com/
    https://www.collinsdictionary.com/us/dictionary/english/the-pits
    
    
    Search Query: perdition
    https://www.merriam-webster.com/dictionary/perdition
    https://www.dictionary.com/browse/perdition
    https://www.vocabulary.com/dictionary/perdition
    
    
    Search Query: blaze
    https://www.blazepizza.com/
    https://www.blazepizza.com/
    
    
    Search Query: nether_region
    https://en.wikipedia.org/wiki/Nether_region
    https://www.merriam-webster.com/dictionary/nether%20parts%2Fregions
    
    
    Search Query: snake_pit
    https://www.instagram.com/snake___pit/?hl=en
    https://www.instagram.com/snakepit_est.2016/?hl=en
    
    
    Search Query: Scheol
    https://www.vocabulary.com/dictionary/Scheol
    https://www.thefreedictionary.com/Scheol
    
    
    Search Query: pit
    https://www.merriam-webster.com/dictionary/pit
    https://flypittsburgh.com/
    
    
    Search Query: underworld
    https://www.imdb.com/title/tt0320691/
    https://en.wikipedia.org/wiki/Underworld_(film_series)
    https://underworldlive.com/
    
    
    Search Query: Inferno
    https://www.imdb.com/title/tt3062096/
    https://en.wikipedia.org/wiki/Inferno_(2016_film)
    
    
    Search Query: hell
    https://en.wikipedia.org/wiki/Hell_in_Christianity
    
    
    

## Complexity<a id="12"></a>
To calculate the complexity of the system based on the given variables, we can develop an equation that takes into account the number of input words, the number of corrected words, the number of synonyms for each word, and the number of searches made. The complexity primarily depends on how these factors interact to produce the final number of results or operations.

Let's define the variables as follows:

- n = number of input words
- c = number of corrected words (assuming each input word can be corrected)
- s = number of synonyms per word
- m = number of searches made

The complexity equation can be outlined as:

- Complexity=(n×s+c)×m

Here's the rationale behind the equation:

Input Words and Synonyms: For each input word, we generate 's' synonyms. So, the total number of outcomes from this part is n×s.

Corrected Words: We add the number of corrected words, 'c'. This assumes that each input word might have a corrected version, which is considered as an additional outcome.

Searches Made: Each combination of words (original, synonyms, and corrected) can lead to a search, so we multiply the above result by the number of searches made, 'm'.

This equation assumes that:

Each word is independent and can have 's' synonyms.
Each word can be corrected, leading to additional outcomes.
Each combination results in a unique search.
This model provides a basic understanding of the system's complexity. However, it's a simplified representation. In practice, the interaction between these variables can be more complex, especially if synonyms and corrections interrelate or if certain combinations of words lead to more or fewer searches.

## Conclusion<a id="14"></a>
The program functions by generating synonyms for each input word and combining these to produce a set of results.  Its operational efficiency is directly tied to the input's complexity and the number of synonyms requested.  For instance, with a single-word input like "hello" having 10 synonyms, the result is straightforward: 10 synonyms plus the original word, yielding 11 outcomes.  However, the scaling becomes more significant with a two-word input such as "hello world".  Here, the program generates synonyms for each word, considering 10 synonyms for each, leading to a multiplication of possibilities.  The total results then become 10 synonyms for 'hello' times 10 for 'world', amounting to 100 combinations, plus 4 additional outcomes for the combination of original and synonymous words.

This illustrates the logarithmic growth in the program's output based on the inputs.  It's crucial to be aware of this exponential increase in results with the addition of more words and synonyms.  Such scaling can lead to a rapid escalation in the number of outcomes, potentially impacting the program's performance and mangeability of the results.  Users should exercise caution when increasing the number of input words and synonyms to avoid overwhelming system resources and to maintin practical usability of the output.
