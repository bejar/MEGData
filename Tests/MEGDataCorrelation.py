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
from scipy import corrcoef
from hcluster import linkage,dendrogram,leaves_list
import networkx as nx
from sklearn.decomposition import PCA,KernelPCA


def correlationMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    for length in range(linit,lend,lstep):
        corrs=corrcoef(mdata[:,length:length+lstep])
        corr+=corrs    
    corr/=nstep
    return corr

def plotSignals(signals,name,cpath,n,m):
    fig = plt.figure()
    fig.set_figwidth(16)
    fig.set_figheight(30)
    i=1
    for s1,s2 in signals:
        plotSignalValues(fig,s1,s2,n,m,i,name)
        i+=1
    fig.savefig(cpath+'/synch-'+name+'.pdf', orientation='landscape',format='pdf')

#    plt.show()



# Plot a set of signals
def plotSignalValues(fig,signal1,signal2,n,m,p,name):
    minaxis=min(signal1)
    maxaxis=max(signal1)
    num=len(signal1)    
    sp1=fig.add_subplot(n,m,p)
    plt.title(str(int(name)+(p)))
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)   
    sp1.plot(t,signal1)
    sp1.plot(t,signal2)
#    plt.show()    


    
cpath='/home/bejar/MEG/Data/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
lnames=['control1-MEG','control2-MEG','control3-MEG','control4-MEG','control5-MEG','control6-MEG','control7-MEG'
        ,'comp1-MEG','comp3-MEG','comp4-MEG' ,'comp5-MEG','comp6-MEG','comp7-MEG','comp13-MEG'
        ,'descomp1-MEG','descomp3-MEG','descomp4-MEG','descomp5-MEG','descomp6-MEG','descomp7-MEG']
name='control1-MEG'


for name in lnames:
    mats=scipy.io.loadmat( cpath+name+'.mat')
    data= mats['data']
    chann= mats['names']

    j=0
    mdata=None
    for i in range(chann.shape[0]):
        cname=chann[i][0][0]
        if cname[0]=='A':
            chndict[cname]=(i,j)
            lnames.append(cname)
            j+=1
            if mdata==None:
                mdata=data[i]
            else:
                mdata=np.vstack((mdata,data[i]))
    
    cmatrix=correlationMatrix(mdata,0,400000,10)

    examp=mp.zeros(j*(j-1)/2-j)
    
    for i in range(data.shape[0]):
        for j in range(i+1,data.shape[0]):
            if np.isnan(corr[i,j]) or corr[i,j]<0.7:
                corr[i,j]=0
#        else:
#            corr[i,j]=1-corr[i,j]
#            print corr[i,j]
    

#print corr
data=np.zeros((data.shape[0],data.shape[0]))
Z=linkage(corr, 'complete')
v=dendrogram(Z, color_threshold=0, orientation='left')
plt.show() 
idl= leaves_list(Z)
for i1,i2 in zip(range(data.shape[0]),idl):
    for j1,j2 in zip(range(data.shape[0]),idl):
        data[i1,j1] = corr[i2,j2]

fig = plt.figure()
fig.set_figwidth(16)
fig.set_figheight(30)
ax = fig.add_subplot(1,1,1)


plt.imshow(data, interpolation='nearest',cmap=cm.gist_yarg)
plt.colorbar(ticks=[-1.0,-0.7,-0.5,-0.3,-0.1,0.0,0.1,0.3,0.5,0.7,1.0], orientation ='horizontal')
plt.show()
fig.savefig(cres+'/distmatrix-T.pdf', orientation='landscape',format='pdf')

#signalGraph=nx.Graph()
#
#for i in range(data.shape[0]):
#    for j in range(data.shape[0]):
#        if corr[i,j]!=0.0 and i!=j:
#            print chann[i][0][0],chann[j][0][0],int(corr[i,j]*100)
#            signalGraph.add_weighted_edges_from([(chann[i][0][0],chann[j][0][0],int(100-(corr[i,j]*100)))])
#       
#
#nx.draw_graphviz(signalGraph)
#plt.show()
#nx.write_graphml(signalGraph, cres+'signalgraph-'+name+'.graphml')
#
