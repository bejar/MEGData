"""
.. module:: ReadData

ReadData
*************

:Description: ReadData

    

:Authors: bejar
    

:Version: 

:Created on: 05/03/2015 9:45 

"""

__author__ = 'bejar'


import mne
from mne.io import read_raw_bti

from config.paths import smaqepath

cont = ['con2/1', 'con3/2', 'con4/1', 'con5/1', 'con6/1', 'con7/1', 'con8/1', 'con9/1', 'con10/1']
comp = ['com1esq1/1', 'com2esq10/1', 'com3esq11/1', 'com4esq12/1', 'com5esq13/1', 'com6esq14/1', 'com7esq15/1',
        'com8esq18/1', 'com9esq19/1', 'com11esq22/1', 'com12esq23/1', 'com13esq24/1']
desc = ['des1esq2/1',  'des3esq4/1', 'des4esq5/2', 'des5esq6/1', 'des6esq7/1', 'des7esq8/1', 'des8esq9/1',
        'des9esq16/1', 'des10esq17/1']

paths = [('control/', cont), ('compensados/', comp), ('descompensados/', desc)]

mne.set_log_level('WARNING')


for pre, con in paths:
    for ind in con:
        indf = pre + ind
        print 'IND=', indf
        a = read_raw_bti(smaqepath + indf + '/e,rfhp1.0Hz', verbose=False)
        print a.info
        print a.ch_names
        print a.n_times

#a.plot(block=True)
