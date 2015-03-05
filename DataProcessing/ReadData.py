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

from mne.io import read_raw_bti

from config.paths import smaqepath


ind = '/ESQcon2/1'

a = read_raw_bti(smaqepath + ind + '/e,rfhp1.0Hz')
