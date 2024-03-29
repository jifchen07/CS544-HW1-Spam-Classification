import sys
import os
import glob
import ast
import time

def main(path):
    txt_files = glob.glob(path + '/**/*.txt', recursive=True)
    model_file = 'nbmodel.txt'

    with open(model_file, 'r', encoding='latin1') as f:
        s = f.read()
        model = ast.literal_eval(s)

    p_w_ham, p_w_spam = model['ham_word_freq'], model['spam_word_freq']

    output_file = 'nboutput.txt'
    with open(output_file, 'w') as f_w:
        for file in txt_files:
            # initialize with P(ham), P(spam)
            p_ham_data, p_spam_data = model['ham_freq'], model['spam_freq']
            with open(file, 'r', encoding='latin1') as f:
                line = f.readline()     # save ram instead of using read()
                while line:
                    for word in line.split():
                        if word in p_w_ham:     # word was seen before in the training data
                            p_ham_data += p_w_ham[word]
                            p_spam_data += p_w_spam[word]
                    line = f.readline()

            if p_ham_data == model['ham_freq']:     # means none of the words were seen before
                print('Undecided ' + file)
            else:
                prediction = 'spam ' if p_ham_data < p_spam_data else 'ham '
                print(prediction + os.path.abspath(file), file=f_w)

    return

if __name__ == '__main__':
    dev_path = './dev'
    if len(sys.argv) > 1:
        dev_path = sys.argv[1]
    start_time = time.time()
    main(path=dev_path)
    print("--- %s seconds ---" % (time.time() - start_time))