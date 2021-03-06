import numpy as np

dir = 'catRawMags1305/catDir/'

# master= np.genfromtxt(dir+'psfPSF_idx_1106_mas.dat')
master= np.genfromtxt(dir+'psfPSF_idx_1506_mas.dat')

f606w = np.genfromtxt(dir+'matchedFLCpsf1506_606.dat') # 606
f814w = np.genfromtxt(dir+'matchedFLCpsf1506_814.dat') #814

# There should be a last column in each catalog giving the index placement

RA, DEC, flags, c_star, magZPT606, magZPTerr606, xPSF_trans606, yPSF_trans606, xPSF_mas606, yPSF_mas606, magPSF606, magErrPSF606, nstar606, id_cat606, id_new606= 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13,14

RA, DEC, flags, c_star, magZPT814, magZPTerr814, xPSF_trans814, yPSF_trans814, xPSF_mas814, yPSF_mas814, magPSF814, magErrPSF814, nstar814, id_cat814, id_new814= 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13,14

x,y,mag606,id606,id814 = 0,1,2,3,4
# Master header
# x y magZ id606 id814

newCols606 = np.zeros((len(master),13))

idCol606 = master[:,id606]
idx606 = np.asarray(idCol606,int)
reg606 = f606w[idx606]

newCols606[:,0] = reg606[:,RA]
newCols606[:,1] = reg606[:,DEC]
newCols606[:,2] = reg606[:,flags]
newCols606[:,3] = reg606[:,c_star]
newCols606[:,4] = reg606[:,magZPT606]
newCols606[:,5] = reg606[:,magZPTerr606]
newCols606[:,6] = reg606[:,xPSF_trans606]
newCols606[:,7] = reg606[:,yPSF_trans606]
newCols606[:,8] = reg606[:,xPSF_mas606]
newCols606[:,9] = reg606[:,yPSF_mas606]
newCols606[:,10] = reg606[:,magPSF606]
newCols606[:,11] = reg606[:,magErrPSF606]
newCols606[:,12] = reg606[:,nstar606]

##################################

newCols814 = np.zeros((len(master),13))
idCol814 = master[:,id814]
idx814 = np.asarray(idCol814,int)
reg814 = f814w[idx814]

newCols814[:,0] = reg814[:,RA]
newCols814[:,1] = reg814[:,DEC]
newCols814[:,2] = reg814[:,flags]
newCols814[:,3] = reg814[:,c_star]
newCols814[:,4] = reg814[:,magZPT814]
newCols814[:,5] = reg814[:,magZPTerr814]
newCols814[:,6] = reg814[:,xPSF_trans814]
newCols814[:,7] = reg814[:,yPSF_trans814]
newCols814[:,8] = reg814[:,xPSF_mas814]
newCols814[:,9] = reg814[:,yPSF_mas814]
newCols814[:,10] = reg814[:,magPSF814]
newCols814[:,11] = reg814[:,magErrPSF814]
newCols814[:,12] = reg814[:,nstar814]

outArr = np.hstack((newCols606,newCols814))
header= 'RA_f606w DEC_f606w flags_f606w c_star_f606w magZPT_f606w magZPTerr_f606w xPSF_trans_f606w yPSF_trans_f606w xPSF_mas_f606w yPSF__fmasw_f606w magPSF_f606w magErrPSF_f606w nstar_f606w RA_f814w DEC_f814w flags_f814w c_star_f814w magZPT_f814w magZPTerr_f814w xPSF_trans_f814w yPSF_trans_f814w xPSF_mas_f814w yPSF_fmasw_f814w magPSF_f814w magErrPSF_f814w nstar_f814w'


# np.savetxt(dir+'matchedPSFpsf1106.dat',outArr,header=header)
np.savetxt(dir+'matchedFLCpsf1506_comb.dat',outArr,header=header)
