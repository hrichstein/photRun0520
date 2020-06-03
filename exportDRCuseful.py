import numpy as np

workDir='./catRawMags1305/catDir/'

drc_dir  = '/Users/hr8jz/Box Sync/Research/source_lists/june13/'
drc = np.genfromtxt(drc_dir + 'HOROLOGIUM-I_sfErr.dat',names=True)

outArr = np.zeros((len(drc),6))

outArr[:,0] = drc['RA_i']
outArr[:,1] = drc['DEC_i']
outArr[:,2] = drc['x_i']
outArr[:,3] = drc['y_i']
outArr[:,4] = drc['magRaw_i']
outArr[:,5] = np.arange(0,len(drc),1)

header = 'RA DEC x y magr id'
form = "%1.7f %1.7f %1.5f %1.5f %1.5f %d"

np.savetxt(workDir+'drc_useful.dat',outArr,header=header,fmt=form)
