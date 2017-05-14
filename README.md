# boggle

Implementation of a Boggle solver web app in Python/Django. See the live version at:
    https://shielded-plains-54627.herokuapp.com/boggle/
    
The majority of the solver logic is in boggle_app/boggle_solver.py. This file contains two classes, one that represents the board and
one that finds all matching words. 

The English-languge word list is found in boggle_app/word_lists/en.txt, and was derived from https://github.com/dwyl/english-words, which
was in turn sourced from http://www.infochimps.com/. The word list was pre-processed using the Django management command defined in
boggle_app/management/commands/scrub_word_list.py to remove all invalid Boggle words.

# Limitations
The code as it stands does not limit the letters available to those that would be found on a standard set of Boggle dice; a user 
could set all letters in the grid to 'Z', which could not occur in the actual game. Additionally, there is no 'QU' combination letter - 
'Q' is treated as any other letter.
