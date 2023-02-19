from sys import platlibdir
from caesar import *
import operator

# This is the list of bigrams, from most frequent to less frequent
bigrams = ["TH", "HE", 'IN', 'OR', 'HA', 'ET', 'AN',
           'EA', 'IS', 'OU', 'HI', 'ER', 'ST', 'RE', 'ND']

# This is the list of monograms, from most frequent to less frequent
monograms = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'D', 'L', 'U',
             'C', 'M', 'F', 'Y', 'W', 'G', 'P', 'B', 'V', 'K', 'X', 'Q', 'J', 'Z']

# This is the dictionary containing the substitution table (e.g. subst_table['A'] = 'B')
# TODO Fill it in the create_subst_table function
subst_table = {}

# These are the dictionaries containing the frequencies of the mono/bigrams in the text
# TODO Fill them in the analyze function
freq_table_bi = {}
freq_table_mono = {}


def sort_dictionary(d):
    """ Sorts a dictionary d by the value. Returns a list of tuples sorted
        by the second element. """
    sorted_dict = list(reversed(sorted(d.items(), key=operator.itemgetter(1))))
    return sorted_dict


def analyze(text):
    """ Computes the frequencies of the monograms and bigrams in the text. """
    global freq_table_mono, freq_table_bi

    # TODO 1.1 Fill in the freq_table_mono dictionary
    for letter in range(0, 26):
        letter_ch = alphabet[letter]
        freq_table_mono[letter_ch] = text.count(letter_ch)

    # TODO 1.2 Fill in the freq_table_bi dictionary
    for first_letter in range(0, len(text) - 1):
        letter_ch = text[first_letter] + text[first_letter + 1]
        freq_table_bi[letter_ch] = text.count(letter_ch)

def create_subst_table():
    """ Creates a substitution table using the frequencies of the bigrams. """
    global subst_table

    # TODO 2.1 Sort the bigrams frequency table by the frequency
    sorted_freq_bi = sort_dictionary(freq_table_bi)

    # TODO 2.2 Fill in the substitution table by associating the sorted frequency
    # dictionary with the given bigrams
    for i in range(0, len(bigrams)):
        (bi, _) = sorted_freq_bi[i]
        first_letter = bi[0]
        second_letter = bi[1]
        if first_letter not in subst_table:
            subst_table[first_letter] = bigrams[i][0]

        if second_letter not in subst_table:
            subst_table[second_letter] = bigrams[i][1]


def complete_subst_table():
    """ Fills in the letters missing from the substitution table using the
        frequencies of the monograms. """
    global subst_table

    # TODO 3.1 Sort the monograms frequency table by the frequency
    sorted_freq_mono = sort_dictionary(freq_table_mono)

    # TODO 3.2 Fill in the missing letters from the substitution table by
    # associating the sorted frequency dictionary with the given monograms
    for i in range(0, len(monograms)):
        (letter, _) = sorted_freq_mono[i]
        if letter not in subst_table:
            subst_table[letter] = monograms[i]


def adjust():
    """ This is magic stuff used in main. """
    global subst_table
    subst_table['Y'] = 'B'
    subst_table['E'] = 'L'
    subst_table['L'] = 'M'
    subst_table['P'] = 'W'
    subst_table['F'] = 'C'
    subst_table['X'] = 'F'
    subst_table['J'] = 'G'
    subst_table['I'] = 'Y'


def decrypt_text(text):
    global subst_table

    # TODO 4 Decrypt and print the text using the substitution table
    plaintext = ''
    subst_table['\n'] = '\n'
    for letter in text:
        plaintext += subst_table[letter]
    
    print(plaintext)


def main():
    with open('msg_ex2.txt', 'r') as myfile:
        text = myfile.read()

    analyze(text)
    create_subst_table()
    complete_subst_table()
    adjust()
    decrypt_text(text)


if __name__ == "__main__":
    main()
