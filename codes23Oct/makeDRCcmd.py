import numpy as np
import matplotlib.pyplot as plt


def makeCMD(targname,dir='./'):

    drc = np.genfromtxt(dir+targname+'_matchedDRCfilt.dat',names=True)

    drc_g = drc.copy()

    fig, ax = plt.subplots(figsize=(4,6.5))

    ax.scatter(drc_g['magr_f606w']-drc_g['magr_f814w'],drc_g['magr_f606w'],s=5)

    ax.set_ylim(28,17.5)
    ax.set_xlim(-1.5,1.5)
    ax.set_xlabel('F606W-F814W')
    ax.set_ylabel('F606W')

    ax.set_title(targname)

    # ax.legend()

    plt.savefig('../drcPhot02Nov/paulCMDs/'+targname+'_drc.png',dpi=600,
                bbox_inches='tight')

    plt.close()

    return None
