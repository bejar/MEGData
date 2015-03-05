# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:41:42 2013

@author: bejar
"""


import scipy.io
from numpy import mean, std
import matplotlib.pyplot as plt
from pylab import *
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score

from scipy import corrcoef

from sklearn.decomposition import PCA,KernelPCA

def plotSignalValues(signal1):
    fig = plt.figure()
    minaxis=min(signal1)
    maxaxis=max(signal1)
    num=len(signal1)  
    print num
    sp1=fig.add_subplot(111)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)   
    sp1.plot(t,signal1)
#    plt.savefig(cres+name)
    plt.show()   


def correlationMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    liter= [linit+(i*lstep) for i in range(nstep)]
#    print liter, len(liter),lend
    zz=0
    for length in liter:
        corrs=corrcoef(mdata[:,length:length+lstep])
        corr+=corrs    
        zz+=1
#        print length, length+lstep,
#    print zz
    corr/=nstep
    return corr


    
cpath='/home/bejar/MEG/Data/'
#cres='/home/bejar/Documentos/Investigacion/MAG/res/'
cres='/home/bejar/Copy/MEG/Correlation/'
##lnames=['control1-MEG','control2-MEG','control3-MEG','control4-MEG','control5-MEG','control6-MEG','control7-MEG'
#        ,'comp1-MEG','comp3-MEG','comp4-MEG' ,'comp5-MEG','comp6-MEG','comp7-MEG','comp13-MEG'
#        ,'descomp1-MEG','descomp3-MEG','descomp4-MEG','descomp5-MEG','descomp6-MEG','descomp7-MEG'
#        ,'control1-MMN','control2-MMN','control3-MMN','control4-MMN','control5-MMN','control6-MMN','control7-MMN'
#        ,'comp1-MMN','comp3-MMN','comp4-MMN' ,'comp5-MMN','comp6-MMN','comp7-MMN','comp13-MMN'
#        ,'descomp1-MMN','descomp3-MMN','descomp4-MMN','descomp5-MMN','descomp6-MMN','descomp7-MMN']
#lcol=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2]
#lnames=['comp10-MEG','comp12-MEG','comp10-MMN','comp12-MMN']
#lcol=[1,1,1,1]
#lband=['alpha','beta','gamma-l','gamma-h','theta','delta','gamma-h']
lnames=['comp1-MEG']
lcol=[1]
lband=['all']
for band in lband:
    examps=None
    print band
    for name in lnames:
        print name
        mats=scipy.io.loadmat( cpath+band+'/'+name+'-'+band+'.mat')
#        mats=scipy.io.loadmat( cpath+'/'+name+'.mat')
        data= mats['data']
        chann= mats['names']
    
        j=0
        mdata=None
        lsnames=[]
        for i in range(chann.shape[0]):
            cname=chann[i][0][0]
#            cname=chann[i]
            if cname[0]=='A' and cname!='A53' and cname!='A31':# and cname!='A44' and cname!='A94':
                j+=1
                lsnames.append(cname)
                if mdata==None:
                    mdata=data[i]
                else:
                    mdata=np.vstack((mdata,data[i]))
#            else:
#                print cname,i
    #    print lsnames
        #cmatrix=correlationMatrix(mdata,0,mdata.shape[1],10)
        print mdata.shape           
        print corrcoef(mdata[[0,2,4],0:1000])
        print lsnames[0:5]
        np.savetxt(cpath+'corr.csv',mdata[[0,2,4],0:1000].transpose(),delimiter=';')
        
#        plotSignalValues(mdata[0,0:1000])
#        plotSignalValues(mdata[2,0:1000])
#        plotSignalValues(mdata[4,0:1000])
    
#    X=examps
#    Y=np.array(lcol)
#    patdata={}
#    patdata['data']=X
#    patdata['classes']=Y
#    scipy.io.savemat(cres+'patcorr-new-loo-'+band,patdata,do_compression=True)
##    scipy.io.savemat(cres+'patcorr-new',patdata,do_compression=True)
#    print
#
