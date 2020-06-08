"""
Zuyue Fu

"""

import scipy
from scipy import io
import networkx
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import sys




def main():
    sys.setrecursionlimit(2000000000)
    filelist = ['data/'+f for f in listdir('data/') if isfile(join('data/', f))]

    optgaps = []

    # only for test;  zuyue 
    # filelist = ['data/dwt_72.mtx']


    res_d = {} # to save optimal matching
    
    for f in range(len(filelist)):
        file = filelist[f]
        print(file)
    
        if file[-4:] != '.mtx':
            continue
    
        #  check optimal matching using networkx
        # extra memory used only to obtain optimal solution
        # read 
        a = scipy.io.mmread(file)
        if not isinstance(a, scipy.sparse.coo_matrix):
            continue
        if a.shape[0] != a.shape[1]:
            tmp = np.array(a.todense())
            nn = max(a.shape)
            a = np.zeros((nn,nn))
            for i in range(len(tmp)):
                for j in range(len(tmp[0])):
                    a[i,j] = tmp[i,j]
                    if i == j:
                        a[i,j] = 0
            a = scipy.sparse.coo_matrix(a)

        a = a.todense()
        for i in range(len(a)):
            for j in range(len(a)):
                if abs(a[i,j]) < 1e-5:
                    a[i,j] = 0
                else:
                    a[i,j] = 1
                if i == j:
                    a[i,j] = 0
        a = scipy.sparse.coo_matrix(a)
    


        # find optimal mathcing to compare 
        # rule out two files: 
        if file == 'data/bayer04.mtx(pass)':  # we pass this file
            opt = 10238
        elif file == 'data/mark3jac020sc.mtx(pass)':  # pass the file
            opt = 4554
        else:  # find optimal matching for ALL 21 graphs
            # construct graph from adj matrix
            g = networkx.convert_matrix.from_numpy_matrix(a.todense())
            # calculate max matching (weight default to be 1)
            opt_matching = networkx.algorithms.matching.max_weight_matching(g)
            # size of the matching
            opt = len(opt_matching)

        res_d[file[5:]] = opt


    with open('optimal_matching.log', 'w') as f:
        print(res_d, file = f)





if __name__ == '__main__':
    main()




