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
        print name
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
            cname=chann[i][0]
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


def filterSignal(data,iband,fband):
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

def correlationMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    liter= [linit+(i*lstep) for i in range(nstep)]
    #print liter, len(liter),lend
    zz=0
    for length in liter:
        corrs=corrcoef(mdata[:,length:length+lstep])
        corr+=corrs    
        zz+=1
        print '.',
    print
    corr/=nstep
    return corr


# Selects a continuous chunk of the file os specific duration width data inside
# a tolerance interval
def selectChunkFile(name,band,duration=1,start=1,tolerance=0.5e-13):
    freq=678.17
    print 'Reading Data: ', name,
    mats=scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'.mat')
    data= mats['data']
    chann= mats['names']
    print ' Processing ...', 
    j=0
    mdata=None
    lcnames=[]
    for i in range(chann.shape[0]):
        cname=chann[i]
        if cname[0]=='A' and not cname.strip() in badchannels:
            j+=1
            lcnames.append(cname.strip())
            if mdata==None:
                mdata=data[i]
            else:
                mdata=np.vstack((mdata,data[i]))
                
    selec=False
    begin=int(freq*start)
    end=begin+int(freq*duration)
    while  not selec:
#      print begin, np.max(mdata[:,begin:end]), np.min(mdata[:,begin:end])
      if  np.all(np.all(mdata[:,begin:end]<tolerance) and  np.all(mdata[:,begin:end]>-tolerance)):
          selec=True
      else:
          begin+=int(freq*duration/10)           
          end+=int(freq*duration/10)
      if end>mdata.shape[1]:
          selec=True
          print 'No Clean Data of that Duration  ------------------------------'
          return
    print 'Begin:',begin,
    patdata={}            
    patdata['data']=mdata[:,begin:end]
    print len(lcnames)
    patdata['names']=lcnames
    patdata['begin']=begin
    patdata['end']=end
    print ' Saving Result ...'
    scipy.io.savemat(cpath+band+'/'+name+'-'+band+'-chunk',patdata,do_compression=True)
    
    
    
# Genrates de data filtering one band
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
        cname=chann[i]
        print cname
        if cname[0]=='A' and not cname.strip() in badchannels:
            j+=1
            lcnames.append(cname.strip())
            if mdata==None:
                mdata=filterSignal(data[i],iband,fband)
            else:
                mdata=np.vstack((mdata,filterSignal(data[i],iband,fband)))
                
    patdata={}            
    patdata['data']=mdata
    patdata['names']=lcnames
    print ' Saving Result ...'
    scipy.io.savemat(cpath+band+'/'+name+'-'+band,patdata,do_compression=True)


# Generates the dataset with the filtered bands
def bandFilter(lband,lnames,badchannels):
    for band,iband,fband in lband: 
        print 'Filtering band: ', band
        for name,_ in lnames:
            bandFilterFile(band,iband,fband,name,badchannels)

# Generates the dataset with a chunk of specific duration
def selectChunk(lnames,lband,duration,start):
    for band,tolerance in lband: 
        print 'Selecting Chunks: ', band
        for name,_ in lnames:
            selectChunkFile(name,band,duration,start,tolerance)
    
## Correlation Matrix Dataset
def correlationDataset(lband,lnames,badchannels,nfile):
    for band,_,_ in lband:
        print 'Dataset for band: ', band
        examps=None
        for name,_ in lnames:
            print 'Reading Data: ', name,
            mats=scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'-chunk'+'.mat')
            data= mats['data']
            chann= mats['names']
            print ' Processing ',         
            j=0
            mdata=None
            lsnames=[]
            for i in range(chann.shape[0]):
                cname=chann[i]
                #print chann[i]
#                print cname,badchannels,cname.strip() in badchannels
                if cname[0]=='A' and not cname.strip() in badchannels:
                    j+=1
                    lsnames.append(cname)
                    if mdata==None:
                        mdata=data[i]
                    else:
                        mdata=np.vstack((mdata,data[i]))
#                else:
#                    print cname,i
#            print mdata.shape
            cmatrix=correlationMatrix(mdata,0,mdata.shape[1],1)
            examp=np.zeros((j*(j-1)/2))
            
            p=0
            for i in range(cmatrix.shape[0]-1):
                for j in range(i+1,cmatrix.shape[0]):
                    examp[p]=cmatrix[i,j]
                    p+=1
                    
            if examps==None:
                examps=examp
            else:
                examps=np.vstack((examps,examp))
        print examps.shape
        X=examps
        Y=np.array([l for _,l in lnames])
        patdata={}
        patdata['data']=X
        patdata['classes']=Y
        print ' Saving Result ...'
        scipy.io.savemat(cres+nfile+'-'+band,patdata,do_compression=True)



cpath='/home/bejar/MEG/DataTest/'
#cpath='/home/bejar/MEG/Data/'
#cres='/home/bejar/MEG/CorrelationTest/'
cres='/home/bejar/Copy/MEG/Correlation/'
#cres='/home/bejar/Documentos/Investigacion/MAG/res/'

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

#lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]

#lnames=[('comp2-MEG',1),('comp2-MMN',1),('comp8-MEG',1),('comp8-MMN',1)
#    ,('comp9-MEG',1),('comp9-MMN',1)
#    ,('control8-MEG',0),('control8-MMN',0),('control9-MEG',0),('control9-MMN',0)  
#    ,('control10-MEG',0),('control10-MMN',0)
#    ,('descomp10-MEG',2),('descomp10-MMN',2)
#    ,('comp12-MEG',2),('comp12-MMN',2),('descomp2-MEG',2),('descomp11-MEG',2)]

# Conjunto de training
#lnames=[('control1-MEG',0),('control2-MEG',0),('control3-MEG',0)
#      ,('control4-MEG',0),('control5-MEG',0),('control6-MEG',0),('control7-MEG',0)
#      ,('comp1-MEG',1),('comp3-MEG',1),('comp4-MEG',1) ,('comp5-MEG',1)
#      ,('comp6-MEG',1),('comp7-MEG',1),('comp13-MEG',1)
#      ,('descomp1-MEG',2),('descomp3-MEG',2),('descomp4-MEG',2),('descomp5-MEG',2)
#      ,('descomp6-MEG',2),('descomp7-MEG',2)]
#lnames=[('comp7-MEG',1)]
#lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]

# Conjunto de test
lnames=[('control8-MEG',0) ,('control9-MEG',0),('control10-MEG',0)
       ,('comp2-MEG',1), ('comp8-MEG',1),('comp9-MEG',1) 
       ,('descomp10-MEG',2),('comp12-MEG',2) ,('descomp2-MEG',2),('descomp11-MEG',2)]
lcol=[0,0,0,1,1,1,2,2,2,2]
# --------------------------------------------------------

#lbandchunk=[('delta',2.0e-12),('gamma-l',1.5e-12),('gamma-h',1.5e-12)]
lbandchunk=[('delta',3.4e-11)]

#lband=[('alpha',8,13),('beta',13,30),('gamma-l',30,60),('gamma-h',60,200),('theta',4,8),('delta',1,4)]
lband=[('gamma-l',30,60),('gamma-h',60,200),('delta',1,4)]
badchannels=['A53','A31','A94']


#channelsNames(lnames)
#badChannels(lnames)

#selectChunk(lnames,lbandchunk,duration=60,start=60)
#bandFilter(lband,lnames,badchannels)
correlationDataset(lband,lnames,badchannels,'patcorr-test-chunk')
