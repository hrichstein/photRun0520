from astropy.io import fits
from astropy import wcs
import numpy as np
from getJdan import getJdan

workDir = './'
upperDir = "/Volumes/Spare Data/Hannah_Data/"

filt_arr = ['F606W', 'F814W']
targname = 'HOROLOGIUM-I'

date = '1305'
catDir = workDir+'catRawMags'+date+'/catDir/'

wcsRA, wcsDEC, flux, flags, c_star, mag1, mag2, mag3, mag4, ra1, dec1, ra2, dec2, ra3, dec3, ra4, dec4, xr1, yr1, xc1, yc1, xt1, yt1, xr2, yr2, xc2, yc2, xt2, yt2, xr3, yr3, xc3, yc3, xt3, yt3, xr4, yr4, xc4, yc4, xt4, yt4 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40

def addTranscols(targname,filt,iter,workDir='./'):

    jdanUse = getJdan(targname,filt)

    if filt=='F606W':
        fils = 'f606w/'
    elif filt=='F814W':
        fils = 'f814w/'

    cat = np.loadtxt(catDir+targname+'_'+filt+'_magList{0:d}.dat'.format(iter))

    newCol = np.zeros((len(cat),12))

    cc = 0
    for jj in range(len(jdanUse)-1):

        if jj==1:
            cc = 3
        elif jj==2:
            cc = 6

        image = fits.open(workDir+targname+'_'+fils+jdanUse[0]+"_flc.fits")
        w = wcs.WCS(header=image[1].header,fobj=image)

        transCat = np.loadtxt(workDir+catDir+jdanUse[jj+1]+"_"+targname+"_"+filt+"_t.dat")

        newCol[:,jj+cc] = transCat[:,0]
        newCol[:,jj+cc+1] = transCat[:,1]
        newCol[:,jj+cc+2], newCol[:,jj+cc+3] = w.wcs_pix2world(newCol[:,jj+cc],newCol[:,jj+cc+1],1)

        image.close()

        # cc = cc + (3-jj)

    cat = np.hstack((cat, newCol))


    header = 'wcsRA wcsDEC flux flags c_star mag1 mag2 mag3 mag4 ra1 dec1 ra2 dec2 ra3 dec3 ra4 dec4 xr1 yr1 xc1 yc1 xt1 yt1 xr2 yr2 xc2 yc2 xo2 yo2 xr3 yr3 xc3 yc3 xo3 yo3 xr4 yr4 xc4 xc4 xo4 yo4 xt2 yt2 wra2 wdec2 xt3 yt3 wra3 wdec3 xt4 yt4 wra4 wdec4'
    form = "%1.7f %1.7f %1.4f %d %1.3f %1.4f %1.4f %1.4f %1.4f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.7f %1.7f %1.4f %1.4f %1.7f %1.7f %1.4f %1.4f %1.7f %1.7f"

    np.savetxt(workDir+catDir+targname+"_"+filt+"_at_long.dat", cat, fmt=form, header=header)

    # print(workDir+catDir+targname+"_"+filt+"_at_long.dat")

    return None

for ff, filt in enumerate(filt_arr):
    addTranscols(targname,filt,iter=1,workDir='./')
