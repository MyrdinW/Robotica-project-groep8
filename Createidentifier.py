import os

# open the output file for writing. will overwrite all existing data in there
with open('neg.txt', 'w') as f:
    # loop over all the filenames
    for filename in os.listdir('data/negatives'):
        f.write('data/negatives/' + filename + '\n')
