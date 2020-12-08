from __future__ import print_function
from glob import glob
import numpy as np

def get_array(fname):
    my_array = []

    f = open('processed_data/{}.ct'.format(fname), "r")
    if f.mode == "r":
        for line in f:
            arr = line.split()
            for i in range(len(arr[0])):
                my_array.append(arr[1])


    f.close()
    return my_array

#my_array = array('CRW_00548')
#print(my_array)


def main(): 

    mat = [[0, 0, 0, 0],
           [0, 0, 0, 0], 
           [0, 0, 0, 0], 
           [0, 0, 0, 0]]


    fnames = glob('processed_data/*.ct')
    for fname in fnames[16:161]:
        pfname = fname[15:-3]
        my_array = get_array(pfname)
        for i in range(len(my_array)-3):
            c1 = int(my_array[i])
            c2 = int(my_array[i+1])
            c3 = int(my_array[i+2])
            c4 = int(my_array[i+3])
            idx1 = 2*c1+c2
            idx2 = 2*c3+c4
            mat[idx1][idx2] += 1

    print('mat is:')
    print(mat)
    sums = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            sums[i] = sums[i] + mat[i][j] 

    probmat = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            probmat[i][j] = 1.*mat[i][j]/sums[i]

    print('probmat:')
    for i in range(4):
        for j in range(4):
            print('{:.3f}'.format(probmat[i][j]), end = ' ')
        print('')

    #print(probmat)


    np.save('probmat.npy', probmat)


main()

