# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:18:50 2013

@author: bejar
"""

import scipy.io
import numpy as np
from scipy import corrcoef
from scipy import signal

def zeroedRange(freq,length,limi,limf):
    nqfreq=freq
    bins=nqfreq/length
    rlimi=limi/bins
    rlimf=limf/bins
    return(int(rlimi),int(rlimf))

def channelsNames(lnames):
    for name,_ in lnames:
        mats=scipy.io.loadmat( cpath+'all/'+name+'-all.mat')
        chann= mats['names']
        for i in range(chann.shape[0]):
            cname=chann[i][0][0]
            if cname[0]=='A':
                print cname
  

def badChannels(lnames):
    for name,_ in lnames:
        print 'Bad Channels: ', name,':',
        mats=scipy.io.loadmat( cpath+'all/'+name+'-all.mat')
        data= mats['data']
        chann= mats['names']
        lchann=[]
        for i in range(chann.shape[0]):
            cname=chann[i][0][0]
            if cname[0]=='A':
                lchann.append(int(cname[1:]))
                if np.mean(data[i])==0.0 or np.std(data[i])==0.0:
                    print cname,
        print len(lchann)
        lschann=sorted(lchann)
        for i in range(len(lschann)-1):
            print lschann[i]
            if lschann[i]!=lschann[i+1]-1:
                print lschann[i]+1,
        print


def filterSignal(data, iband, fband):
    freq=678.17/2
    if iband==1:
        b,a=scipy.signal.butter(8,fband/freq,btype='low')
        flSignal=scipy.signal.filtfilt(b, a, data)
    else:
        b,a=scipy.signal.butter(8,iband/freq,btype='high')
        temp=scipy.signal.filtfilt(b, a, data)
        b,a=scipy.signal.butter(8,fband/freq,btype='low')
        flSignal=scipy.signal.filtfilt(b, a, temp)
    return flSignal


def correlationMatrix(mdata, linit, lend, nstep):
    lstep = (lend - linit) / nstep
    corr = np.zeros((mdata.shape[0], mdata.shape[0]))
    liter = [linit + (i*lstep) for i in range(nstep)]
    #print liter, len(liter),lend
    zz=0
    for length in liter:
        corrs = corrcoef(mdata[:,length:length+lstep])
        corr += corrs
        zz += 1
        print '.',
    print
    corr /= nstep
    return corr


def bandFilterFile(band,iband,fband,name,badchannels):
    print 'Reading Data: ', name,
    mats=scipy.io.loadmat( cpath+'all/'+name+'.mat')
    data= mats['data']
    chann= mats['names']
    print ' Processing ...', 
    j=0
    mdata=None
    lcnames=[]
    for i in range(chann.shape[0]):
        cname=chann[i][0][0]
        if cname[0]=='A' and not cname.strip() in badchannels:
            j+=1
            lcnames.append(cname.strip())
            if mdata==None:
                mdata=filterSignal(data[i],iband,fband)
            else:
                mdata=np.vstack((mdata,filterSignal(data[i],iband,fband)))
                
    patdata={}            
    patdata['data']=mdata
    print lcnames,len(lcnames)
    patdata['names']=lcnames
    print ' Saving Result ...'
    scipy.io.savemat(cpath+band+'/'+name+'-'+band,patdata,do_compression=True)


# Generates the dataset with the filtered bands
def bandFilter(lband,lnames,badchannels):
    for band,iband,fband in lband: 
        print 'Filtering band: ', band
        for name,_ in lnames:
            bandFilterFile(band,iband,fband,name,badchannels)


    
## Correlation Matrix Dataset
def correlationDataset(lband, lnames, badchannels, nfile, window=10, nex=1):
    for band,_,_ in lband:
        print 'Dataset for band: ', band
        examps = None
        expnames = []
        llabels = []
        for name, l in lnames:
            print 'Reading Data: ', name
            #print cpath+band+'/'+name+'-'+band+'.mat'
            mats = scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'.mat')
            #mats = scipy.io.loadmat(cpath+band+'/'+name+'.mat')
            data = mats['data']
            chann = mats['names']
            print ' Processing '
            nchan = 0
            mdata=None
            lsnames = []
            for i in range(chann.shape[0]):
                cname = chann[i]
                # print cname,badchannels,cname.strip() in badchannels
                if cname[0] == 'A' and not cname.strip() in badchannels:
                    nchan += 1
                    lsnames.append(cname)
                    if mdata is None:
                        mdata = data[i]
                    else:
                        mdata = np.vstack((mdata, data[i]))
#                else:
#                    print cname,i
            #print mdata.shape,
            print 'Channels:' , nchan
            chunksize = mdata.shape[1]//nex
            linit = 0
            for iex in range(nex):
                print 'Chunk ', iex,
                expnames.append(name + '-' + str(iex))
                llabels.append(l)
                cmatrix = correlationMatrix(mdata, linit, linit+chunksize, window)
                linit += chunksize

                examp = np.zeros((nchan * (nchan - 1) / 2))

                p = 0
                for i in range(cmatrix.shape[0]-1):
                    for j in range(i + 1, cmatrix.shape[0]):
                        examp[p] = cmatrix[i, j]
                        p += 1

                if examps is None:
                    examps = examp
                else:
                    examps = np.vstack((examps, examp))
        
        X = examps
        patdata = {}
        patdata['data'] = X
        patdata['classes'] = llabels
        patdata['examples'] = expnames
        print ' Saving Result ...', X.shape
        scipy.io.savemat(cres + nfile + '-' + band + '-w' + str(window), patdata, do_compression=True)



cpath='/home/bejar/MEG/Data/'
#cpath='/home/bejar/MEG/Data/'
#cres='/home/bejar/MEG/CorrelationTest/'
cres='/home/bejar/Copy/MEG/Correlation/'
#cres='/home/bejar/Documentos/Investigacion/MAG/res/'

# Train
#lnames=[('control1-MEG',0),('control2-MEG',0),('control3-MEG',0),('control4-MEG',0)
#        ,('control5-MEG',0),('control6-MEG',0),('control7-MEG',0)
#        ,('comp1-MEG',1),('comp3-MEG',1),('comp4-MEG',1) ,('comp5-MEG',1)
#        ,('comp6-MEG',1),('comp7-MEG',1),('comp13-MEG',1)
#        ,('descomp1-MEG',2),('descomp3-MEG',2),('descomp4-MEG',2),('descomp5-MEG',2)
#        ,('descomp6-MEG',2),('descomp7-MEG',2)
#        ,('control1-MMN',0),('control2-MMN',0),('control3-MMN',0),('control4-MMN',0)
#        ,('control5-MMN',0),('control6-MMN',0),('control7-MMN',0)
#        ,('comp1-MMN',1),('comp3-MMN',1),('comp4-MMN',1) ,('comp5-MMN',1)
#        ,('comp6-MMN',1),('comp7-MMN',1),('comp13-MMN',1)
#        ,('descomp1-MMN',2),('descomp3-MMN',2),('descomp4-MMN',2),('descomp5-MMN',2)
#        ,('descomp6-MMN',2),('descomp7-MMN',2)]


#lnames=[('control1-MMN',0),('control2-MMN',0),('control3-MMN',0),('control4-MMN',0)
#        ,('control5-MMN',0),('control6-MMN',0),('control7-MMN',0)
#        ,('comp1-MMN',1),('comp3-MMN',1),('comp4-MMN',1) ,('comp5-MMN',1)
#        ,('comp6-MMN',1),('comp7-MMN',1),('comp13-MMN',1)
#        ,('descomp1-MMN',2),('descomp3-MMN',2),('descomp4-MMN',2),('descomp5-MMN',2)
#        ,('descomp6-MMN',2),('descomp7-MMN',2)]


# Train
#lnames=[('comp2-MEG',1),('comp2-MMN',1),('comp8-MEG',1),('comp8-MMN',1)
#    ,('comp9-MEG',1),('comp9-MMN',1)
#    ,('control8-MEG',0),('control8-MMN',0),('control9-MEG',0),('control9-MMN',0)  
#    ,('control10-MEG',0),('control10-MMN',0)
#    ,('descomp10-MEG',2),('descomp10-MMN',2)
#    ,('comp12-MEG',2),('comp12-MMN',2),('descomp2-MEG',2),('descomp11-MEG',2)]

# Test
# lnames=[('control8-MMN',0),('control9-MMN',0),('control10-MMN',0)
#        ,('comp2-MMN',1),('comp8-MMN',1),('comp9-MMN',1)
#        ,('descomp10-MMN',2),('comp12-MMN',2)]

# All
lnames = [
        ('control1-MEG',0), ('control1-MMN',0),
        ('control2-MEG',0), ('control2-MMN',0),
        ('control3-MEG',0), ('control3-MMN',0),
        ('control4-MEG',0), ('control4-MMN',0),
        ('control5-MEG',0), ('control5-MMN',0),
        ('control6-MEG',0), ('control6-MMN',0),
        ('control7-MEG',0), ('control7-MMN',0),
        ('control8-MEG',0), ('control8-MMN',0),
        ('control9-MEG',0), ('control9-MMN',0),
        ('control10-MEG',0), ('control10-MMN',0),
        ('comp1-MEG',1), ('comp1-MMN',1),
        ('comp2-MEG',1), ('comp2-MMN',1),
        ('comp3-MEG',1), ('comp3-MMN',1),
        ('comp4-MEG',1), ('comp4-MMN',1),
        ('comp5-MEG',1), ('comp5-MMN',1),
        ('comp6-MEG',1), ('comp6-MMN',1),
        ('comp7-MEG',1), ('comp7-MMN',1),
        ('comp8-MEG',1), ('comp8-MMN',1),
        ('comp9-MEG',1), ('comp9-MMN',1),
        ('comp13-MEG',1), ('comp13-MMN',1),
        ('descomp1-MEG',2), ('descomp1-MMN',2),
        ('descomp3-MEG',2), ('descomp3-MMN',2),
        ('descomp4-MEG',2), ('descomp4-MMN',2),
        ('descomp5-MEG',2), ('descomp5-MMN',2),
        ('descomp6-MEG',2), ('descomp6-MMN',2),
        ('descomp7-MEG',2), ('descomp7-MMN',2),
        ('descomp10-MEG',2), ('descomp10-MMN',2),
        #('comp12-MEG',2),
        #('comp12-MMN',2)
]



#lband=[('alpha',8,13),('beta',13,30),('gamma-l',30,60),('gamma-h',60,200),('theta',4,8),('delta',1,4)]
lband = [('gamma-l',30,60),('gamma-h',60,200)]

#lnames=[('control5-MEG',0)]

#lnames=[('control1-MEG',0),('control2-MEG',0),('control3-MEG',0),('control4-MEG',0)
#        ,('control5-MEG',0),('control6-MEG',0),('control7-MEG',0)
#        ,('comp1-MEG',1),('comp3-MEG',1),('comp4-MEG',1) ,('comp5-MEG',1)
#        ,('comp6-MEG',1),('comp7-MEG',1),('comp13-MEG',1)
#        ,('descomp1-MEG',2),('descomp3-MEG',2),('descomp4-MEG',2),('descomp5-MEG',2)
#        ,('descomp6-MEG',2),('descomp7-MEG',2)]
#lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]

#badchannels=['A53','A31','A44','A94']
badchannels=['A53','A31','A94']
#channelsNames(lnames)
#badChannels(lnames)
#bandFilter(lband,lnames,badchannels)
correlationDataset(lband, lnames, badchannels, 'patcorr-all-MEG-MMN-2chunks', window=10, nex=2)

