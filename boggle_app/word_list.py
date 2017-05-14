# English word list derived from:
#   https://github.com/dwyl/english-words
# originally sourced from
#   http://www.infochimps.com/

# Word lists pre-processed using
#    manage.py scrub_word_list
# to remove words with non-ascii characters and words with < 3 or > 16
# characters, and to convert all words to lowercase.

from marisa_trie import Trie

class WordList(object):
    def __init__(self, word_file):
        # TODO: Check input file exists, is readable, valid, etc
        words = []
        with open(word_file) as input_file:
            for word in input_file:
                words.append(word.lower().strip())
        self.trie = Trie(words)

    def contains_word(self, word):
        """
        Check whether a word exists in the list.
        
        :param word: An ASCII, lowercase string to check for.
        :return: True if the word is in the word list, false if it is not.
        """
        # TODO: Raise errors if the word is None, isn't ASCII or lowercase, etc
        return word in self.trie

    def contains_prefix(self, prefix):
        """
        Check list for words that begin with the supplied prefix
        
        :param prefix: An ASCII, lowercase string to check as a prefix
        :return: True if this key is a prefix for some other word or words in 
        the list. Note that this method will return False if the word is in the
        list but is not a prefix of any other word.
        """
        # TODO: Raise errors if prefix is None, isn't ASCII or lowercase, etc
        return len(self.trie.keys(prefix)) > 1

en_us = WordList('boggle_app/word_lists/en.txt')
