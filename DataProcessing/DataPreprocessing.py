"""
.. module:: DataPreprocessing

DataPreprocessing
*************

:Description: DataPreprocessing

    

:Authors: bejar
    

:Version: 

:Created on: 09/03/2015 8:35 

"""

__author__ = 'bejar'

import numpy as np
import mne
from mne.io import read_raw_bti
import scipy.io
import logging

from config.paths import smaqepath, datapath

con = ['con2/1', 'con3/2', 'con4/1', 'con5/1', 'con6/1', 'con7/1', 'con8/1', 'con9/1', 'con10/1']
comp = ['com1esq1/1', 'com2esq10/1', 'com3esq11/1', 'com4esq12/1', 'com5esq13/1', 'com6esq14/1', 'com7esq15/1',
        'com8esq18/1', 'com9esq19/1', 'com12esq23/1', 'com13esq24/1']
desc = ['des1esq2/1',  'des3esq4/1', 'des4esq5/2', 'des5esq6/1', 'des6esq7/1', 'des7esq8/1', 'des10esq17/1']

lband = [('alpha', 8, 13), ('beta', 13, 30), ('gamma-l', 30, 60),
         ('gamma-h', 60, 200), ('theta', 4, 8), ('delta', 1, 4)]

clasif = {
    'con2/1': 0, 'con3/2': 0, 'con4/1': 0, 'con5/1': 0, 'con6/1': 0, 'con7/1': 0, 'con8/1': 0, 'con9/1': 0,
    'con10/1': 0,
    'com1esq1/1': 1, 'com2esq10/1': 1, 'com3esq11/1': 1, 'com4esq12/1': 1, 'com5esq13/1': 1, 'com6esq14/1': 1,
    'com7esq15/1': 1, 'com8esq18/1': 1, 'com9esq19/1': 1, 'com13esq24/1': 1,
    'des1esq2/1': 2,  'des3esq4/1': 2, 'des4esq5/2': 2, 'des5esq6/1': 2, 'des6esq7/1': 2, 'des7esq8/1': 2,
    'des10esq17/1': 2, 'com12esq23/1': 2
}

paths = [('control/', con), ('compensados/', comp), ('descompensados/', desc)]

#mne.set_log_level('WARNING')

logger = logging.getLogger('log')
console = logging.StreamHandler()
logging.getLogger('log').addHandler(console)

# print a.ch_names
# print len(a)
# print a[0][0]
# print len(a[0][0])
# print len(a[0][1])
# print a.info

for pre, con in paths:
    for ind in con:

        logger.info('Individual %s', ind)
        indf = pre + ind

        a = read_raw_bti(smaqepath + indf + '/e,rfhp1.0Hz', verbose=False)

        for band, lf, hf in lband:
            fa = mne.filter.band_pass_filter(a)

            nchannels = len([cn for cn in a.info['ch_names'] if 'MEG' in cn])
            data = np.zeros((nchannels, len(a)))
            lcnames = []
            ic = 0
            for i, cn in enumerate(a.ch_names):
                if 'MEG' in cn:
                    #print cn
                    lcnames.append(cn)
                    data[ic] = a[i][0][0]
                    ic += 1

            filedata = {'channels': lcnames, 'data': data}
            nfile = ind.split('/')[0]

            scipy.io.savemat(datapath + 'DataT3/All/' + 'T3-' + nfile, filedata, do_compression=True)
