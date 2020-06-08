"""
Zuyue Fu

"""

import scipy
from scipy import io
import networkx
from os import listdir
from os.path import isfile, join
from myalgo import greedy, algo
import numpy as np
import logging
import argparse
import os


parser = argparse.ArgumentParser(description='matching')
parser.add_argument(
    '--niter',
    type=int,
    default=1,
    help='total number of iterations')

parser.add_argument(
    '--seed',
    type=int,
    default=42,
    help='random seed')

parser.add_argument(
    '--logfile',
    type=str,
    default='logmatching.log',
    help='log file')


def main():
    args = parser.parse_args()
    np.random.seed(args.seed)

    logging.basicConfig(filename=args.logfile, level=logging.INFO)

    logging.info('Find max matching for different graphs.')
    logging.info('')

    filelist = ['data/'+f for f in listdir('data/') if isfile(join('data/', f))]

    args = parser.parse_args()

    optgaps = []

    with open('optimal_matching.log', 'r') as f:
        opt_matching = eval(f.read())



    # only for test;  zuyue 
    # filelist = ['data/dwt_72.mtx']
    
    for f in range(len(filelist)):
        file = filelist[f]
    
        if file[-4:] != '.mtx':
            continue
    
        # read 
        a = scipy.io.mmread(file)
        if not isinstance(a, scipy.sparse.coo_matrix):
            logging.info(str(type(a)) + ': not a coo_matrix!')
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
            logging.info('matrix nrow not match ncol! fill with zeros')

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



        # get size of optimal matching from file
        opt = opt_matching[file[5:]]
    
    
    
        # get all edges: cannot exceed 30% of them
        alledges = np.array(a.nonzero()).T
        n = len(a.todense())
        m = len(alledges)
    
        #############################################
        ##  This is the beginning of my algorithm  ##
        ##  No extra memory will be used here      ##
        #############################################
        maxgap = 0
        # init matching as empty list
        mymatching = [] # list of sets
        # covered vertices
        cvertex = set()

        ind = list(range(m))

        for niter in range(args.niter):
            np.random.shuffle(ind)
            # no more than 30% edges CALLED BY ALGO
            greedy(alledges[ind[:int(0.3*m)]], mymatching, cvertex, m, n)
            algo(alledges[ind[:int(0.3*m)]], mymatching, cvertex, m, n)
            greedy(alledges[ind[int(0.3*m):int(0.6*m)]], mymatching, cvertex, m, n)
            algo(alledges[ind[int(0.3*m):int(0.6*m)]], mymatching, cvertex, m, n)
            greedy(alledges[ind[int(0.6*m):int(0.9*m)]], mymatching, cvertex, m, n)
            algo(alledges[ind[int(0.6*m):int(0.9*m)]], mymatching, cvertex, m, n)
            greedy(alledges[ind[int(0.9*m):]], mymatching, cvertex, m, n)
            algo(alledges[ind[int(0.9*m):]], mymatching, cvertex, m, n)

            mylen = len(mymatching)

            if maxgap < mylen:
                maxgap = mylen

            if niter % 1000 == 0:
                logging.info("%18s: iter %5d, Optimal %5d, Current %5d" % (file[5:], niter, opt, maxgap))

            # only to save CPU time
            if mylen == opt:
                break

        gap = 0
        if opt > 0:
            gap = (opt-mylen)/opt
        optgaps.append(gap)
        logging.info("%18s: Optimal %5d, Current Best %5d" % (file[5:], opt, maxgap))
        logging.info('########################################################################')
        logging.info('########################################################################')
        logging.info('########################################################################')
        logging.info('########################################################################')

        folder = 'matching_res_' + str(args.niter) + '/'

        try: 
            os.mkdir(folder) 
        except OSError as error: 
            pass

        filen = folder + file[5:-4] + '_matching.log'
        with open(filen, 'w') as f:
            print(mymatching, file = f)
            print('niter: %d. Optimal: %d. Our: %d. With %d edges missing, and gap: %.3f' % (args.niter, opt, mylen, (opt-mylen), gap), file = f)




    '''
    logging.info('####################################')
    logging.info('## iter #%5d: ave opt gap %.3f ##' % (niter+1, np.mean(optgaps)))
    logging.info('####################################')
    '''
    logging.info(optgaps)
    logging.info('Best Ave Opt Gap: %.6f' % np.mean(optgaps))
    logging.info('Standard Deviation: %.6f' % np.std(optgaps))


if __name__ == '__main__':
    main()
