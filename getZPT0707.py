import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def getZPT(targname,filt,dir='./',sigTol=2.5,stdTol=0.05):


    # file = np.genfromtxt(dir+'flcDRCmatch_'+filt+'.dat',names=True)
    file = np.genfromtxt(dir+'flcDRCmatch_'+filt+'_mDc.dat',names=True)
    drc = np.genfromtxt(dir+'drc_useful_'+targname+'.dat')

    lenD = len(drc)

    kG = True # keep going

    # Loop to try to make sure I'm basing the magnitude correction off of a decent amount of stars.
    while kG:

        file_g = file[file['stdF']<=stdTol]
        # file_g = file[file_idx]

        flc_diff = stats.sigmaclip(file_g['magrD']-file_g['magrF'],sigTol,sigTol)

        if len(flc_diff[0]) >= (0.1*lenD):
            kG = False

        else:
            stdTol += 0.05
            sigTol += 0.25

        if (stdTol >= 0.5) or (sigTol >= 3.5):
            print('Not very good stats. Need more stars.')
            kG = False

    mag_corr = np.nanmean(flc_diff[0])
    err_add = np.nanstd(flc_diff[0] / np.sqrt(len(flc_diff[0])))

    # plotting part

    fig, ax = plt.subplots(figsize=(6,4))

    ax.scatter(file_g['magrD'],file_g['magrD']-file_g['magrF'],s=20)
    ax.hlines(mag_corr,17.5,28)

    ax.set_xlim(17.5,28)
    title_str = targname + '_' + filt + ' {0}'.format(len(flc_diff[0]))
    ax.set_title(title_str)

    # plt.savefig(dir+targname+'_'+filt+'ZPTline.png',dpi=600,bbox_inches='tight')
    plt.savefig(dir+targname+'_'+filt+'ZPTline_mdC.png',dpi=600,bbox_inches='tight')

    plt.close()

    return mag_corr, err_add


def applyZPT(mag_corr,err_add,targname,filt,dir='./'):

    # all = np.genfromtxt(dir+'magSTDcutAll_'+filt+'.dat',names=True)
    # cat = np.genfromtxt(dir+'magSTDcutAll_'+filt+'.dat')
    all = np.genfromtxt(dir+'magSTDcutAll_'+filt+'_mDc.dat',names=True)
    cat = np.genfromtxt(dir+'magSTDcutAll_'+filt+'_mDc.dat')

    mean = all['mean']
    std = all['stdev']

    new_mag = mean + mag_corr
    new_err = np.sqrt ( std**2 + err_add**2)

    newCol = np.zeros((len(all),2))
    newCol[:,0] = new_mag
    newCol[:,1] = new_err

    outArr = np.hstack((cat,newCol))

    colAs = np.array(all.dtype.names)
    s0=' '
    header = s0.join(colAs)
    header += ' magZPT magZPTerr'

    # form = '%1.7f %1.7f %1.4f %d %1.3f %1.4f %1.4f %1.4f %1.4f '
    # form +='%1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.4f %1.4f '
    # form +='%1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f '
    # form +='%1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f '
    # form +='%1.4f %1.4f %1.4f %1.5f %d %d %d %1.4f %1.5'

    # np.savetxt(dir+'magZPTedAll_'+filt+'.dat',outArr,header=header)
    np.savetxt(dir+'magZPTedAll_'+filt+'_mDc.dat',outArr,header=header)


    return None


def doZPT(targname,filt,dir='./',sigTol=2.5,stdTol=0.05):

    mag_corr,err_add = getZPT(targname,filt,dir=dir,sigTol=2.5,stdTol=0.05)

    applyZPT(mag_corr,err_add,targname,filt,dir=dir)


    return None
#
