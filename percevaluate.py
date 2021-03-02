import sys
import time

def safe_divide(x, y):
    return x / y if y else 0

def main(path):
    T = {'ham': 0, 'spam': 0}
    F = {'ham': 0, 'spam': 0}
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            predict, path = line.split()
            if 'ham' in path or 'spam' in path:
                if predict in path:
                    T[predict] += 1
                else:
                    F[predict] += 1
            # if no label found in path, don't increment
            line = f.readline()

    print(T['ham'], T['spam'], F['ham'], F['spam'])

    precision_spam = safe_divide(T['spam'], T['spam'] + F['spam'])
    precision_ham = safe_divide(T['ham'], T['ham'] + F['ham'])
    recall_spam = safe_divide(T['spam'], T['spam'] + F['ham'])
    recall_ham = safe_divide(T['ham'], T['ham'] + F['spam'])
    F1_spam = safe_divide(2 * precision_spam * recall_spam, precision_spam + recall_spam)
    F1_ham = safe_divide(2 * precision_ham * recall_ham, precision_ham + recall_ham)

    print('1a. spam precision: {:.2f}%'.format(precision_spam * 100))
    print('1b. spam recall: {:.2f}%'.format(recall_spam * 100))
    print('1c. spam F1 score: {:.2f}'.format(F1_spam))
    print('1a. ham precision: {:.2f}%'.format(precision_ham * 100))
    print('1b. ham recall: {:.2f}%'.format(recall_ham * 100))
    print('1c. ham F1 score: {:.2f}'.format(F1_ham))
    return

if __name__ == '__main__':
    output_path = 'percoutput.txt'
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    start_time = time.time()
    main(path=output_path)
    print("--- %s seconds ---" % (time.time() - start_time))