# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:15:59 2013

@author: bejar
"""

import scipy.io
import numpy as np
from scipy import corrcoef
from sklearn.cluster import spectral_clustering,affinity_propagation
import matplotlib.pyplot as plt
from pylab import *
from sklearn.metrics import silhouette_score
from sklearn.manifold import spectral_embedding
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D

def correlationMatrix(mdata,linit,lend,nstep):
    lstep=(lend-linit)/nstep
    corr=np.zeros((mdata.shape[0],mdata.shape[0]))
    for length in range(linit,lend,lstep):
        corrs=corrcoef(mdata[:,length:length+lstep])
        corr+=corrs    
    corr/=nstep
    return corr
    
    
def modelSelection(inc,fnc):
    for nc in range(inc,fnc):        
        labels = spectral_clustering(cmatrix, n_clusters=nc, eigen_solver='arpack',assign_labels='discretize')
        
        #for j in range(nclusters):
        #    print j
        #    cllab=[]
        #    for i in range(len(lnames)):
        #        if labels[i]==j:
        #            cllab.append(lnames[i])
        #    print sort(cllab)
        #    print '\n---'
        
        dmatrix=cmatrix.copy()
        
        for i in range(dmatrix.shape[0]):
            for j in range(cmatrix.shape[1]):
                    dmatrix[i,j]=1-cmatrix[i,j]
                
        print nc,':', silhouette_score(dmatrix,labels,metric='precomputed')
    
cpath='/home/bejar/MEG/Data/'
cres='/home/bejar/Documentos/Investigacion/MEG/res/'
#name='MMN-201205251030'
name='control1-MMN'
mats=scipy.io.loadmat( cpath+name+'.mat')
data= mats['data']
chann=mats['names']

chndict={}
lnames=[]
j=0
mdata=None
for i in range(chann.shape[0]):
    cname=chann[i][0][0]
    if cname[0]=='A' and cname!='A53' and cname!='A31':
        chndict[cname]=(i,j)
        lnames.append(cname)
        j+=1
        if mdata==None:
            mdata=data[i]
        else:
            mdata=np.vstack((mdata,data[i]))

for i in lnames:
    print i
    
cmatrix=correlationMatrix(mdata,0,400000,10)

corrmin=0.1
for i in range(cmatrix.shape[0]):
    for j in range(cmatrix.shape[1]):
        if cmatrix[i,j]<0:
            #cmatrix[i,j]=-cmatrix[i,j]
            cmatrix[i,j]=0
            
            
Pr=spectral_embedding(cmatrix,n_components=3)

labels = spectral_clustering(cmatrix, n_clusters=6, eigen_solver='arpack',assign_labels='discretize')
#clcen,labels=affinity_propagation(cmatrix,damping=0.5)


cm_bright = ListedColormap(['#000000','#FF0000','#00FF00','#0000FF','#FF00FF'
                            ,'#FFFF00','#00FFFF','#9999FF','#FF9999','#99FF99'])
#print Pr            

fig = plt.figure()

ax = fig.add_subplot(1,1,1, projection='3d')

plt.scatter(Pr[:,0],Pr[:,1],zs=Pr[:,2],c=labels,cmap=cm_bright,s=25,marker='o')


for s in ['A1','A71','A134','A145','A139','A140']:
    _,pos1=chndict[s]
    plt.scatter(Pr[pos1,0],Pr[pos1,1],zs=Pr[pos1,2],c=labels[pos1],cmap=cm_bright,s=100,marker='^')


#plt.imshow(cmatrix, interpolation='nearest',cmap=cm.gist_yarg)
#plt.colorbar(ticks=[-1.0,-0.7,-0.5,-0.3,-0.1,0.0,0.1,0.3,0.5,0.7,1.0], orientation ='horizontal')
plt.show()

