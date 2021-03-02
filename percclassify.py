import sys
import os
import glob
import ast
import time

def main(path):
    txt_files = glob.glob(path + '/**/*.txt', recursive=True)
    model_file = 'percmodel.txt'

    with open(model_file, 'r', encoding='latin1') as f:
        s = f.read()
        model = ast.literal_eval(s)

    b, w = model['bias'], model['weights']

    output_file = 'percoutput.txt'
    with open(output_file, 'w') as f_w:
        for file in txt_files:
            y = 0
            with open(file, 'r', encoding='latin1') as f:
                line = f.readline()
                while line:
                    for word in line.split():
                        if word in w:
                            y += w[word]
                    line = f.readline()

            prediction = 'spam ' if y > 0 else 'ham '
            print(prediction + os.path.abspath(file), file=f_w)
    return

if __name__ == '__main__':
    dev_path = './dev'
    if len(sys.argv) > 1:
        dev_path = sys.argv[1]
    start_time = time.time()
    main(path=dev_path)
    print("--- %s seconds ---" % (time.time() - start_time))