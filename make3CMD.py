""" Making CMDs to compare photometry apertures/techniques """

import numpy as np
import matplotlib.pyplot as plt


def make3CMD(targname,):

    se_dir = './catMatchFLCdrc18Oct/seDRCs/'
    se_file = se_dir + targname + '_sfErr.dat'

    pu3_dir = './photUtils21Oct/catDir_' + targname + '/'
    pu3_file = pu3_dir + targname + '_allMatchedZPTed_pu.dat'

    pu4dir = './catRawMags20Aug/catDir_' + targname + './'
    pu4_file = pu4dir + targname + '_allMatchedZPTed_pu.dat'

    se_3pix = np.genfromtxt(se_file,names=True)
    pu_3pix = np.genfromtxt()
    pu_4pix = np.genfromtxt()


    return None





#
