"""
.. module:: DataExtraction

DataExtraction
*************

:Description: DataExtraction

    

:Authors: bejar
    

:Version: 

:Created on: 22/04/2015 14:09 

"""

__author__ = 'bejar'

import numpy as np
import scipy.io
from config.paths import datapath
import operator


lnames = [
    ('control1-MEG', 0), ('control1-MMN', 0),
    ('control2-MEG', 0), ('control2-MMN', 0),
    ('control3-MEG', 0), ('control3-MMN', 0),
    ('control4-MEG', 0), ('control4-MMN', 0),
    ('control5-MEG', 0), ('control5-MMN', 0),
    ('control6-MEG', 0), ('control6-MMN', 0),
    ('control7-MEG', 0), ('control7-MMN', 0),
    ('control8-MEG', 0), ('control8-MMN', 0),
    ('control9-MEG', 0), ('control9-MMN', 0),
    ('control10-MEG', 0), ('control10-MMN', 0),
    ('comp1-MEG', 1), ('comp1-MMN', 1),
    ('comp2-MEG', 1), ('comp2-MMN', 1),
    ('comp3-MEG', 1), ('comp3-MMN', 1),
    ('comp4-MEG', 1), ('comp4-MMN', 1),
    ('comp5-MEG', 1), ('comp5-MMN', 1),
    ('comp6-MEG', 1), ('comp6-MMN', 1),
    ('comp7-MEG', 1), ('comp7-MMN', 1),
    ('comp8-MEG', 1), ('comp8-MMN', 1),
    ('comp9-MEG', 1), ('comp9-MMN', 1),
    ('comp13-MEG', 1), ('comp13-MMN', 1),
    ('descomp1-MEG', 2), ('descomp1-MMN', 2),
    ('descomp3-MEG', 2), ('descomp3-MMN', 2),
    ('descomp4-MEG', 2), ('descomp4-MMN', 2),
    ('descomp5-MEG', 2), ('descomp5-MMN', 2),
    ('descomp6-MEG', 2), ('descomp6-MMN', 2),
    ('descomp7-MEG', 2), ('descomp7-MMN', 2),
    ('descomp10-MEG', 2), ('descomp10-MMN', 2),
#    ('comp12-MEG', 2), ('comp12-MMN', 2),
]


freq = 678.17
lband = [('gamma-l', 30, 60)]
badchannels = ['A53', 'A31', 'A94']
size = int(freq*100)

for band, _, _ in lband:
    for name, _ in lnames:
        mats = scipy.io.loadmat(datapath + 'Data/' + band + '/' + name + '-' + band + '.mat')
        data = mats['data']
        chann = mats['names']
        lchan = []
        nchan = 0
        for i, ch in enumerate(chann):
            if 'A' in ch and not ch.strip() in badchannels:
                lchan.append((int(ch.strip()[1:]), i))
        lchan = sorted(lchan, key=operator.itemgetter(0))
        matrix = np.zeros((len(lchan), size))
        i = 0
        for _, j in lchan:
            matrix[i] = data[j, size:size*2]
            i += 1


        scipy.io.savemat(datapath+'/VC/'+ band + '/' + name + '-' + band + '.mat', {'data': matrix}, do_compression=True)
