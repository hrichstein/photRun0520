import numpy as np
from scipy import stats

dir = 'catRawMags1305/catDir/'

f814w = np.genfromtxt('flcDRC0506_magCut.dat',names=True)
cat = np.genfromtxt('flcDRC0506_magCut.dat')

flc_diff = stats.sigmaclip(f814w['magDRC']-f814w['mean'],2.5,2.5)

err_add = np.std(flc_diff[0] / np.sqrt(len(flc_diff[0])))

new_err = np.sqrt( f814w['stdev']**2 + err_add**2 )

mag_corr = np.nanmean(flc_diff[0])

new_mag = f814w['mean'] + mag_corr

newCol = np.zeros((len(cat),2))
newCol[:,0] = new_mag
newCol[:,1] = new_err

out = np.hstack((cat,newCol))

header = 'RA DEC flags c_star mag1 mag2 mag3 mag4 xt1 yt1 xDRC_trans yDRC_trans xDRC_mat yDRC_mat magDRC id_cat mean stdev cut_flag idx_cut num_abv_std magZPT magZPTerr'

np.savetxt(dir+'flcDRC0506_zptMags.dat',out,header=header)
