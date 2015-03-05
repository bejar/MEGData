# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:41:42 2013

@author: bejar
"""


import scipy.io
from numpy import mean, std
import matplotlib.pyplot as plt
from pylab import *
from numpy.fft import rfft, irfft 
from  matplotlib.backends.backend_pdf import PdfPages


regions={'sup':['A2','A3','A4','A5','A6','A7','A8','A9',
                'A10','A11','A12','A13','A14','A15','A16',
                'A17','A18','A19','A20','A21','A22','A23',
                'A24','A25','A26','A27','A28','A29'],
         'front': ['A30','A31','A32',
                  'A48','A49','A50','A51','A52',
                  'A69','A70','A71','A72','A73','A74',
                  'A92','A93','A94'],
         'tempi': ['A33','A34','A35','A36','A37',
                  'A53','A54','A55','A56','A57',
                  'A75','A76','A77','A78','A79','A80',
                  'A95','A96','A97','A98','A99','A100',
                  'A113','A114','A115','A116','A117','A118',
                  'A131','A132','A133','A134','A135','A136'],
        'tempd': ['A43','A44','A45','A46','A47',
                 'A64','A65','A66','A67','A68',
                 'A86','A87','A88','A89','A90','A91',
                 'A107','A108','A109','A110','A111','A112',
                 'A125','A126','A127','A128','A129','A130',
                 'A143','A144','A145','A146','A147','A148'],
         'occip': ['A38','A39','A40','A41','A42',
                 'A58','A59','A60','A61','A62','A63'
                 'A81','A82','A83','A84','A85',
                 'A101','A102','A103','A104','A105','A106',
                 'A119','A120','A121','A122','A123','A124',
                 'A137','A138','A139','A140','A141','A142']
                
        }


def plotSignals(signals,cpath,n,m):
    fig = plt.figure()
    fig.set_figwidth(16)
    fig.set_figheight(30)
    i=1
    for s,snm in signals:
        if min(s)!=max(s):
            plotSignalValues(fig,s,n,m,i,snm)
        else:
            plotDummy(fig,len(s),n,m,i,snm)
        i+=1
    fig.savefig(pp, orientation='landscape',format='pdf')

#    plt.show()



# Plot a set of signals
def plotSignalValues(fig,signal1,n,m,p,name):
    minaxis=min(signal1)
    maxaxis=max(signal1)
    num=len(signal1)    
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)   
    sp1.plot(t,signal1)
#    plt.show()    

def plotDummy(fig,num,n,m,p,name):
    minaxis=-1
    maxaxis=1
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)   
    sp1.plot(t,t)
#    plt.show()    

    


def plotSignalFile(name):
    mats=scipy.io.loadmat( cpath+name+'-'+banda+'.mat')
    data= mats['data']
    chann=mats['names']
    freq=40
    off=60000
    length=60000
    for i in range(0,data.shape[0]+1,20):
        lsignals=[]
        for j in range(i,i+20):
            if j<data.shape[0]:
                # copy the current segment
                orig=data[j][off:off+length]
                lsignals.append((orig,chann[j]))
        plotSignals(lsignals,cres,10,2)
    
    
banda='delta'
cpath='/home/bejar/MEG/DataTest/'+banda+'/'
cres='/home/bejar/Documentos/Investigacion/MAG/res/'
#name='MMN-201205251030'
lname=['control10-MEG']

for name in lname:
    pp = PdfPages(cres+'/synch-'+name+'-'+banda+'.pdf')
    plotSignalFile(name)
    pp.close()
