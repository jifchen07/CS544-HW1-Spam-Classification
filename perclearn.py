import sys
import glob
import collections
import random

def main(path):
    txt_files = glob.glob(path + '/**/*.txt', recursive=True)
    max_iter = 100
    w = collections.defaultdict(float)
    u = collections.defaultdict(float)
    b = beta = 0
    cnt = 1

    for i in range(max_iter):
        print('training iteration {}'.format(i))
        # shuffle data
        random.shuffle(txt_files)
        for file in txt_files:
            if 'ham' not in file and 'spam' not in file:
                continue
            y_t = 1 if 'spam' in file else -1

            y = b
            cache = []
            with open(file, 'r', encoding='latin1') as f:
                # calculate y
                line = f.readline()
                while line:
                    for word in line.split():
                        y += w[word]
                        cache.append(word)
                    line = f.readline()
                # update weights
                if y * y_t <= 0:
                    b += y_t
                    beta += y_t * cnt
                    for word in cache:
                        w[word] += y_t
                        u[word] += y_t * cnt

            cnt += 1

    # generate the final parameters
    beta = b - (1/cnt) * beta
    for word in u.keys():
        u[word] = round(w[word] - u[word] / cnt, 8)

    # store parameters
    dict_all = {'bias': beta, 'weights': dict(u)}

    model_file = 'percmodel.txt'
    with open(model_file, 'w', encoding='latin1') as f:
        f.write(str(dict_all))

    return

if __name__ == '__main__':
    src_path = './train'
    if len(sys.argv) > 1:
        src_path = sys.argv[1]
    main(path=src_path)