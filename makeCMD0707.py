import numpy as np
import matplotlib.pyplot as plt

def makeCMD(targname,dir='./'):

    drc = np.genfromtxt(dir+'drc_useful_'+targname+'.dat',names=True)

    flc = np.genfromtxt(dir+targname+'_sourceList0720.dat',names=True)

    d_idx = np.logical_and(drc['c_star_f606w']>=0.5, drc['c_star_f814w']>=0.5)
    f_idx = np.logical_and(flc['c_star_f606w']>=0.5, flc['c_star_f814w']>=0.5)
    
    drc_g = drc[d_idx]
    flc_g = flc[f_idx]

    fig, ax = plt.subplots(figsize=(4,6.5))

    ax.scatter(drc_g['magr_f606w']-drc_g['magr_f814w'],drc_g['magr_f606w'],s=5,label='DRC')
    ax.scatter(flc_g['magZPT_f606w']-flc_g['magZPT_f814w'],flc_g['magZPT_f606w'],s=5,label='FLC')

    ax.set_ylim(28,17.5)
    ax.set_xlim(-1.5,1.5)
    ax.set_xlabel('F606W-F814W')
    ax.set_ylabel('F606W')

    ax.set_title(targname)

    ax.legend()

    plt.savefig(dir+targname+'_cmd.png',dpi=600,bbox_inches='tight')

    plt.close()

    return None
