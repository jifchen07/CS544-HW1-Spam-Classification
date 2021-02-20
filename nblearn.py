import sys
import glob
from math import log10 as log
from collections import Counter


def main(path):
    txt_files = glob.glob(path + '/**/*.txt', recursive=True)

    word_counts_ham, word_counts_spam = Counter(), Counter()
    num_ham, num_spam = 0, 0

    for file in txt_files:
        if 'ham' in file:
            word_counts = word_counts_ham
            num_ham += 1
        elif 'spam' in file:
            word_counts = word_counts_spam
            num_spam += 1
        else:
            print('unclassified file')
            continue

        with open(file, 'r', encoding='latin1') as f:
            lines = f.read().splitlines()   # .splitlines() used to remove tailing \n
            for line in lines:
                word_counts.update(Counter(line.split(' ')))

    # added 1 smoothing
    word_counts_all_one = {token: 1 for token in (word_counts_ham + word_counts_spam).keys()}
    word_counts_ham += word_counts_all_one
    word_counts_spam += word_counts_all_one
    words_total_ham, words_total_spam = sum(word_counts_ham.values()), sum(word_counts_spam.values())

    # calculate P(wi|ham) and P(wi|spam) after smoothing
    word_freq_ham = {token: round(log(cnt / words_total_ham), 8) for token, cnt in word_counts_ham.items()}
    word_freq_spam = {token: round(log(cnt / words_total_spam), 8) for token, cnt in word_counts_spam.items()}

    # calculate P(ham), P(spam) and add them to the dicts so they can be written to file easily
    num_total = num_ham + num_spam

    dict_all = {'ham_freq': log(num_ham / num_total), 'ham_word_freq': word_freq_ham,
                'spam_freq': log(num_spam / num_total), 'spam_word_freq': word_freq_spam}

    model_file = 'nbmodel.txt'
    with open(model_file, 'w', encoding='latin1') as f:
        f.write(str(dict_all))

    return




if __name__ == '__main__':
    src_path = './train'
    if len(sys.argv) > 1:
        src_path = sys.argv[1]
    main(path=src_path)
