import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from sklearn.linear_model import LinearRegression
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import binned_statistic

def masterFeed(targname,dir='./'):

    # feedFunc1(targname,dir=dir)
    # feedFunc2(targname,dir=dir)
    # feedFunc3(targname,dir=dir)
    # feedFunc4(targname,dir=dir)
    # feedFunc5(targname,dir=dir)
    # feedFunc6(targname,dir=dir)
    # feedFunc7(targname,dir=dir)
    # feedFunc8(targname,dir=dir)
    feedFunc9(targname,dir=dir)


    return None

# PSF-DRC
def feedFunc1(targname,dir='./',name='psf2drc'):

    dir2 = dir + 'matchedCutFiles/'

    file = np.genfromtxt(dir2+'psf2drc.dat',names=True)

    make9plots(file['m606c'],file['m814c'],file['magr_f606w'],file['magr_f814w'],'PSF','DRC',saveDir=dir2,name=name)


    return None


# APER-DRC
def feedFunc2(targname,dir='./',name='aper2drc'):

    dir2 = dir + 'matchedCutFiles/'

    file = np.genfromtxt(dir2+'aper2drc.dat',names=True)

    make9plots(file['m606c'],file['m814c'],file['magr_f606w'],file['magr_f814w'],'APER','DRC',saveDir=dir2,name=name)


    return None


# OLD - NEW
def feedFunc3(targname,dir='./',name='newOldflc'):

    dir2 = dir + 'matchedCutFiles/'

    match = np.genfromtxt(dir2+'flcOldNew.dat',names=True)

    make9plots(match['magr_f606wO'],match['magr_f814wO'],match['magr_f606wN'],match['magr_f814wN'],'Old FLCs','New FLCs',saveDir=dir2,name=name)

    return None


# PSF-FLC
def feedFunc4(targname,dir='./',name='psf2flc'):

    dir2 = dir + 'matchedCutFiles/'

    file = np.genfromtxt(dir2+'psf2flc.dat',names=True)

    make9plots(file['m606c'],file['m814c'],file['magZPT_f606w'],file['magZPT_f814w'],'PSF','FLC',saveDir=dir2,name=name)


    return None


# DRC OLD - NEW
def feedFunc5(targname,dir='./',name='oldNewDRC'):

    dir2 = dir + 'matchedCutFiles/'

    match = np.genfromtxt(dir2+'drcOldNew.dat',names=True)

    make9plots(match['magRaw_v'],match['magRaw_i'],match['magr_f606w'],match['magr_f814w'],'Old DRC','New DRC',saveDir=dir2,name=name)

    return None


# DRC - FLC (no ZPT)
def feedFunc6(targname,dir='./',name='DRC2flcNoZPT'):

    dir2 = dir + 'matchedCutFiles/'

    match = np.genfromtxt(dir2+'flc2drcNoZPT.dat',names=True)

    make9plots(match['magr_f606w'],match['magr_f814w'],match['mean_f606w'],match['mean_f814w'],'DRC','FLC no ZPT',saveDir=dir2,name=name)

    return None


# DRC - FLC
def feedFunc7(targname,dir='./',name='DRC2flc'):

    dir2 = dir + 'matchedCutFiles/'

    match = np.genfromtxt(dir2+'flc2drc.dat',names=True)

    make9plots(match['magr_f606w'],match['magr_f814w'],match['magZPT_f606w'],match['magZPT_f814w'],'DRC','FLC',saveDir=dir2,name=name)

    return None


def feedFunc8(targname,dir='./',name='aper2flc'):

    dir2 = dir + 'matchedCutFiles/'

    file = np.genfromtxt(dir2+'aper2flc.dat',names=True)

    make9plots(file['m606c'],file['m814c'],file['magZPT_f606w'],file['magZPT_f814w'],'APER','FLC',saveDir=dir2,name=name)


    return None


def feedFunc9(targname,dir='./',name='FLC2flcNoZPT'):

    dir2 = dir + 'matchedCutFiles/'

    match = np.genfromtxt(dir2+'flc2drcNoZPT.dat',names=True)

    make9plots(match['magZPT_f606w'],match['magZPT_f814w'],match['mean_f606w'],match['mean_f814w'],'FLC','FLC no ZPT',saveDir=dir2,name=name)

    return None

def make9plots(arr1_v,arr1_i,arr2_v,arr2_i,str1,str2,saveDir='./',name=None):

    arr1_c = arr1_v - arr1_i
    arr2_c = arr2_v - arr2_i

    # Binning Process

    bin_means1, bin_edges1, binnum1= binned_statistic(arr1_v, arr2_v-arr1_v, bins=10, range=(19.5, 24.5),statistic='mean')
    bin_width = (bin_edges1[1] - bin_edges1[0])
    bin_cent1 = bin_edges1[1:] - bin_width/2

    bin_means2, bin_edges2, binnum2= binned_statistic(arr1_i, arr2_i-arr1_i, bins=10, range=(19.5, 24.5),statistic='mean')

    bin_width = (bin_edges2[1] - bin_edges2[0])
    bin_cent2 = bin_edges2[1:] - bin_width/2

    bin_means3, bin_edges3, binnum3= binned_statistic(arr1_c, arr2_c-arr1_c, bins=10, range=(-1,2.5),statistic='mean')

    bin_width = (bin_edges3[1] - bin_edges3[0])
    bin_cent3 = bin_edges3[1:] - bin_width/2

    bin_means4, bin_edges4, binnum4= binned_statistic(arr1_v, arr2_v-arr1_v, bins=10, range=(19.5,24.5),statistic='std')

    bin_width = (bin_edges4[1] - bin_edges4[0])
    bin_cent4 = bin_edges4[1:] - bin_width/2

    bin_val4 = bin_means4/np.sqrt(len(arr1_v))

    bin_means5, bin_edges5, binnum5= binned_statistic(arr1_i,  arr2_i-arr1_i, bins=10, range=(19.5,24.5),statistic='std')

    bin_width = (bin_edges5[1] - bin_edges5[0])
    bin_cent5 = bin_edges5[1:] - bin_width/2

    bin_val5 = bin_means5/np.sqrt(len(arr1_i))

    bin_means6, bin_edges6, binnum6= binned_statistic(arr1_c, arr2_c-arr1_c, bins=10, range=(-1,2.5),statistic='std')

    bin_width = (bin_edges6[1] - bin_edges6[0])
    bin_cent6 = bin_edges6[1:] - bin_width/2

    bin_val6 = bin_means6/np.sqrt(len(arr1_c))


    median1 = np.median(stats.sigmaclip(arr2_v-arr1_v,4,4)[0])
    median2 = np.median(stats.sigmaclip(arr2_i-arr1_i,4,4)[0])
    median3 = np.median(stats.sigmaclip(arr2_c-arr1_c,4,4)[0])


    # Plotting Part

    plt.rcParams['axes.grid'] = True

    fig, ((ax1,ax2,ax3), (ax4,ax5,ax6), (ax7,ax8,ax9)) = \
    plt.subplots(3,3,figsize=(18,18))

    ax1.scatter(arr1_v,arr2_v-arr1_v,s=2)
    ax1.set_xlim(18,24.5)
    ax1.set_ylim(-0.15,0.15)
    ax1.hlines(median1,18,29,color='red',label='median={0:.3f}'.format(median1))
    ax1.set_ylabel('V {0} - V {1} [mag]'.format(str2,str1))
    ax1.set_xlabel('V {0} [mag]'.format(str1))
    ax1.legend()

    ax2.scatter(arr1_i,arr2_i-arr1_i,s=2)
    ax2.set_xlim(18,24.5)
    ax2.set_ylim(-0.15,0.15)
    ax2.hlines(median2,18,29,color='red',label='median={0:.3f}'.format(median2))
    ax2.set_ylabel('I {0} - I {1} [mag]'.format(str2,str1))
    ax2.set_xlabel('I {0} [mag]'.format(str1))
    ax2.legend()

    ax3.scatter(arr1_c,arr2_c-arr1_c,s=2)
    ax3.set_xlim(-1,2.5)
    ax3.set_ylim(-0.15,0.15)
    ax3.hlines(median3,-1,2.5,color='red',label='median={0:.3f}'.format(median3))
    ax3.set_ylabel('(V-I) {0} - (V-I) {1} [mag]'.format(str2,str1))
    ax3.set_xlabel('(V-I) {0} [mag]'.format(str1))
    ax3.legend()

    ax4.scatter(bin_cent1,bin_means1,s=30,color='red')
    ax4.set_xlim(18,24.5)
    ax4.set_ylim(-0.03,0.06)
    ax4.set_ylabel('mean({0}-{1}) [mag]'.format(str2,str1))
    ax4.set_xlabel('V {0} [mag]'.format(str1))

    ax5.scatter(bin_cent2,bin_means2,s=30,color='red')
    ax5.set_xlim(18,24.5)
    ax5.set_ylim(-0.03,0.06)
    ax5.set_ylabel('mean({0}-{1}) [mag]'.format(str2,str1))
    ax5.set_xlabel('I {0} [mag]'.format(str1))

    ax6.scatter(bin_cent3,bin_means3,s=30,color='red')
    ax6.set_xlim(-1,2.5)
    # ax6.set_ylim(-0.03,0.06)
    ax6.set_ylabel('mean({0}-{1}) [mag]'.format(str2,str1))
    ax6.set_xlabel('(V-I) {0} [mag]'.format(str1))

    ax7.scatter(bin_cent4,bin_val4,s=30,color='blue')
    ax7.set_xlim(18,24.5)
    ax7.set_ylim(-0.0005,0.014)
    ax7.set_xlabel('V {0} [mag]'.format(str1))
    ax7.set_ylabel(r'$\sigma$/sqrt(N)({0}-{1}) [mag]'.format(str2,str1))

    ax8.scatter(bin_cent5,bin_val5,s=30,color='blue')
    ax8.set_xlim(18,24.5)
    ax8.set_ylim(-0.0005,0.014)
    ax8.set_xlabel('I {0} [mag]'.format(str1))
    ax8.set_ylabel(r'$\sigma$/sqrt(N)({0}-{1}) [mag]'.format(str2,str1))

    ax9.scatter(bin_cent6,bin_val6,s=30,color='blue')
    ax9.set_xlim(-1,2.5)
    ax9.set_ylim(-0.0005,0.014)
    ax9.set_xlabel('(V-I) {0} [mag]'.format(str1))
    ax9.set_ylabel(r'$\sigma$/sqrt(N)({0}-{1}) [mag]'.format(str2,str1))


    # plt.show()
    plt.savefig(saveDir+'ninePlots_'+name+'.png',dpi=600,bbox_inches='tight')

    plt.close()
    return None
