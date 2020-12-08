from glob import glob
import numpy as np

def get_array(fname):
    col1 = []
    col2 = []
    f= open('processed_data/{}.ct'.format(fname), "r")
    if f.mode == 'r':
        for line in f:
            arr = line.split()
            for i in range(len(arr[0])):
                col1.append(arr[0])
                col2.append(arr[1])
    f.close()
    return col1, col2


def main():
    
    mat = [[0 for _ in range(16)] for _ in range(4)]

    c2i = {'A':0, 'C':1, 'G':2, 'U':3}

    fnames = glob('processed_data/*.ct')
    for fname in fnames[16:161]:
        pfname = fname[15:-3]
        col1, col2 = get_array(pfname)
        for i in range(len(col1)-1):
            x1 = c2i[col1[i]]
            x2 = c2i[col1[i+1]]
            y1 = int(col2[i])
            y2 = int(col2[i+1])
   
            row = 2*y1 + y2
            col = 4*x1 + x2
                   
            mat[row][col] += 1
            
    print('mat is:')
    print(mat)
    #sums = [0 for _ in range(16)]
    sums = [0]*16
    for i in range(4):
        for j in range(16):
            sums[j] = sums[j] + mat[i][j]

    emprobmat = [[0 for _ in range(16)] for _ in range(4)]
    for i in range(4):
        for j in range(16):
            emprobmat[i][j] = mat[i][j]/sums[j]

    print('emprobmat:')
    #print(emprobmat)
    for i in range(4):
        for j in range(16):
            print(f'{emprobmat[i][j]:.3f}', end=' ')
            #print('{:.3f}'.format(emprobmat[i][j], 
        print('')

    np.save('emprobmat.npy', emprobmat)




main()
