import numpy as np
import matplotlib.pyplot as plt
from linear6d import *

def linDRConTrans(targname,dir='photUtils0820/'):

    # Going from APER to FLC_pu

    file = np.genfromtxt(dir+'oldNewDRCref_'+targname+'_1408.dat',names=True)
    fileCat = np.genfromtxt(dir+'oldNewDRCref_'+targname+'_1408.dat')
    colNs = np.array(file.dtype.names)


    drc_dir  = '/Users/hr8jz/Box Sync/Research/source_lists/june13/'
    all = np.genfromtxt(drc_dir + 'HOROLOGIUM-I_sfErr.dat',names=True)
    allCat = np.genfromtxt(drc_dir + 'HOROLOGIUM-I_sfErr.dat')
    colAs = np.array(all.dtype.names)

    # Putting the APER positions into the match array to be used as references transformed
    match_arr = np.zeros((len(file),2))
    xa_2p = np.int(np.where(colNs=='x_old')[0])
    ya_2p = np.int(np.where(colNs=='y_old')[0])

    match_arr[:,0] = fileCat[:,xa_2p]
    match_arr[:,1] = fileCat[:,ya_2p]

    # Putting the PU positions into the master array
    master_arr = np.zeros((len(file),2))
    xp = np.int(np.where(colNs=='x_new')[0])
    yp = np.int(np.where(colNs=='y_new')[0])

    master_arr[:,0] = fileCat[:,xp]
    master_arr[:,1] = fileCat[:,yp]

    weights = np.zeros((len(master_arr)))
    weights.fill(1.0)

    # Filling the array with values to be transformed
    all_arr = np.zeros((len(all),2))

    x_bt = np.int(np.where(colAs=='x_v')[0])
    y_bt = np.int(np.where(colAs=='y_v')[0])

    all_arr[:,0] = allCat[:,x_bt]
    all_arr[:,1] = allCat[:,y_bt]

    outName = dir + targname + "_oldDRC2newTrans"

    new_match, new_all = test_linear(match_arr[:,0],match_arr[:,1], master_arr[:,0], master_arr[:,1], weights, weights, all_arr[:,0],all_arr[:,1])


    outArr = np.hstack((allCat,new_all))

    s0=' '
    header = s0.join(colAs)
    header += ' x_Trans y_Trans'

    # np.savetxt(outName+'.dat',outArr,header=header)
    np.savetxt(outName+'_1408.dat',outArr,header=header)

    makePlot(targname,match_arr[:,0],match_arr[:,1],\
    new_match[:,0],new_match[:,1],master_arr[:,0], master_arr[:,1],label_1='Original in OLD',label_2='New in OLD 2 NEW',label_3='Original in NEW',outname=outName+'_matchCheck')

    return None


def makePlot(targname,x1,y1,x2,y2,x3,y3,label_1,\
    label_2,label_3,outname):

    fig, ax = plt.subplots(figsize=(6,6))

    ax.scatter(x3,y3,label=label_3,s=70)
    # ax.scatter(x1,y1,label=label_1,s=50)
    ax.scatter(x2,y2,label=label_2,s=20)

    ax.legend()
    ax.set_title(targname)

    # plt.savefig(outname+'.png',dpi=600,bbox_inches='tight')
    plt.savefig(outname+'_1408.png',dpi=600,bbox_inches='tight')
    plt.close()


    return None
