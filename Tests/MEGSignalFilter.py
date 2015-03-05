# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:15:25 2013

@author: bejar
"""

import scipy.io
import numpy as np
from scipy import signal


def zeroedRange(freq,length,limi,limf):
    nqfreq=freq
    bins=nqfreq/length
    rlimi=limi/bins
    rlimf=limf/bins
    return(int(rlimi),int(rlimf))


def filterSignal(data,iband,fband):
    if iband==1:
        b,a=scipy.signal.butter(8,fband/freq,btype='low')
        flSignal=scipy.signal.filtfilt(b, a, data)
    else:
        b,a=scipy.signal.butter(8,iband/freq,btype='high')
        temp=scipy.signal.filtfilt(b, a, data)
        b,a=scipy.signal.butter(8,fband/freq,btype='low')
        flSignal=scipy.signal.filtfilt(b, a, temp)
    return flSignal

cpath='/home/bejar/MEG/Data/'
#lnames=['control1-MEG']
#lnames=['control1-MEG','control2-MEG','control3-MEG','control4-MEG','control5-MEG','control6-MEG','control7-MEG'
#        ,'comp1-MEG','comp3-MEG','comp4-MEG' ,'comp5-MEG','comp6-MEG','comp7-MEG','comp13-MEG'
#        ,'descomp1-MEG','descomp3-MEG','descomp4-MEG','descomp5-MEG','descomp6-MEG','descomp7-MEG'
#        ,'control1-MMN','control2-MMN','control3-MMN','control4-MMN','control5-MMN','control6-MMN','control7-MMN'
#        ,'comp1-MMN','comp3-MMN','comp4-MMN' ,'comp5-MMN','comp6-MMN','comp7-MMN','comp13-MMN'
#        ,'descomp1-MMN','descomp3-MMN','descomp4-MMN','descomp5-MMN','descomp6-MMN','descomp7-MMN']
#lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]
lnames=['comp10-MEG','comp12-MEG','comp10-MMN','comp12-MMN']
lcol=[1,1,1,1]

freq=678.17/2
#lband=[('alpha',8,13),('beta',13,30),('gamma-l',30,60),('gamma-h',60,200),('theta',4,8),('delta',1,4)]
lband=[('delta',1,4)]
for band,iband,fband in lband: 
    cres='/home/bejar/MEG/Data/'+band+'/'
    for name in lnames:
        print name
        mats=scipy.io.loadmat( cpath+name+'.mat')
        data= mats['data']
        chann= mats['names']
    
        j=0
        mdata=None
        lcnames=[]
        for i in range(chann.shape[0]):
            cname=chann[i][0][0]
            if cname[0]=='A' and cname!='A53' and cname!='A31' and cname!='A44' and cname!='A94':
                j+=1
                lcnames.append(cname)
                if mdata==None:
                    mdata=filterSignal(data[i],iband,fband)
                else:
                    mdata=np.vstack((mdata,filterSignal(data[i],iband,fband)))
            #else:
            #    print cname,i
                    
        patdata={}            
        patdata['data']=mdata
        patdata['names']=lcnames
        scipy.io.savemat(cres+name+'-'+band,patdata,do_compression=True)



