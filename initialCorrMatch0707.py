import numpy as np
import os
from astropy.io import fits
import time

from getJdan import getJdan
from f2mag0707 import f2mag_dirs
from hst_func import *
from linTrans import *

upperDir = "/Volumes/Spare Data/Hannah_Data/"
offset = 20.0 # number of pixels in one arcsecond
# seDir, magCatDir, catDir = f2mag_dirs(targname,date='1305',workDir='./')

def distCor(targname,filt,workDir='./'):

    jdanUse = getJdan(targname,filt)

    for ff in range(len(jdanUse)):
        #Load catalog
        cat = np.genfromtxt(workDir+ jdanUse[ff]+'_'+targname+'_'+filt+'_wMag.dat',names=True)
        catCat = np.loadtxt(workDir+ jdanUse[ff]+'_'+targname+'_'+filt+'_wMag.dat')
        #Do correction
        cor = acsDistortion(upperDir+'wfc_'+filt,cat['xr'],cat['yr'])
        #Add columns
        cat = np.hstack((catCat,cor))

        header = "flags RA DEC xr yr flux c_star magr id xc yc"
        form = "%d %1.7f %1.7f %1.4f %1.4f %1.4f %1.3f %1.4f %d %1.4f %1.4f"

        np.savetxt(workDir+jdanUse[ff]+'_'+targname+'_'+filt+'_dc.dat',cat,fmt=form,header=header)


    return None


def offCor(targname,filt,workDir='./'):

    jdanUse = getJdan(targname,filt)

    if filt=='F606W':
        fils = 'f606w/'
    elif filt=='F814W':
        fils = 'f814w/'

    for jj, jdan in enumerate(jdanUse):

        # Load images, retrieve offset info
        tempim = fits.open(targname+'_'+fils+jdan+"_flc.fits")

        xoff = float(tempim[0].header["POSTARG1"])
        yoff = float(tempim[0].header["POSTARG2"])

        tempim.close()

        # Load the respective catalog
        cat = np.genfromtxt(workDir+jdan+"_"+targname+"_"+filt+"_dc.dat",names=True)
        catCat = np.loadtxt(workDir+jdan+"_"+targname+"_"+filt+"_dc.dat")

        # Create an array for the new values
        newCol = np.zeros((len(cat),2))

        # Apply offsets to columns
        newCol[:,0] = cat['xc'] - (offset * xoff)
        newCol[:,1] = cat['yc'] - (offset * yoff)

        # Combine to single array and save out
        cat = np.hstack((catCat, newCol))

        header = "flags RA DEC xr yr flux c_star magr id xc yc xo yo"
        form = "%d %1.7f %1.7f %1.4f %1.4f %1.4f %1.3f %1.4f %d %1.4f %1.4f %1.4f %1.4f"

        np.savetxt(workDir+jdan+"_"+targname+"_"+filt+"_oc.dat",cat,header=header,fmt=form)


    return None

# Specifically for first run through
def matchWJCs(targname,filt,workDir='./',matchtol=2):

    # xt, yt = 11,12
    # magr,id = 7,8

    jdanUse = getJdan(targname,filt)
    outName = "master_ids_"+targname+"_"+filt+"_0.dat"

    master = np.genfromtxt(workDir+jdanUse[0]+"_"+targname+'_'+filt+"_oc.dat",names=True)
    masterCat = np.loadtxt(workDir+jdanUse[0]+"_"+targname+'_'+filt+'_oc.dat')

    colNs = np.array(master.dtype.names)

    xt = np.int(np.where(colNs=='xo')[0])
    yt = np.int(np.where(colNs=='yo')[0])
    xtstr = 'xo'
    ytstr = 'yo'

    magr = np.int(np.where(colNs=='magr')[0])
    id = np.int(np.where(colNs=='id')[0])
    # Create an array of zeros with columns equal to the number of non-master dithers to store the matching id for each source
    matchids = np.zeros((len(master), (len(jdanUse)-1)))
    # master = np.hstack((masterCat, matchids))

    # Loop through other images
    for dd in range(len(jdanUse)-1):
        # Load catalogs
        cat = np.genfromtxt(workDir+jdanUse[dd+1]+"_"+targname+'_'+filt+'_oc.dat',names=True)
        catCat = np.loadtxt(workDir+jdanUse[dd+1]+"_"+targname+'_'+filt+'_oc.dat')

        nF = True
        row = 0

        while (nF): # not finished
            matchrows = cat[(abs(master[row][xtstr] - cat[xtstr]) <= matchtol) & (abs(master[row][ytstr] - cat[ytstr]) <= matchtol)]

    #         # Setting the proper column number to the matching index.
            if (len(matchrows) == 1):
              matchids[row][dd] = matchrows[0][id]
              row = row + 1

            elif (len(matchrows) > 1):
                magDif = np.zeros((len(matchrows),1))
                for mm in range(len(matchrows)):
                    magDif[mm] = master[row][magr] - matchrows[mm][magr]
                    small = np.argmin(magDif)
                    matchids[row][dd] = matchrows[small][id]
                row += 1

            else:
              master = np.delete(master, row, 0)
              masterCat = np.delete(masterCat, row, 0)
              matchids = np.delete(matchids,row,0)

            if (row >= len(master)):
                nF = False

    outArr = np.hstack((masterCat,matchids))

    header =  "flags RA DEC xr yr flux c_star magr id xc yc xt yt id2 id3 id4"
    form = "%d %1.7f %1.7f %1.4f %1.4f %1.4f %1.3f %1.4f %d %1.4f %1.4f %1.4f %1.4f %d %d %d"

    print(targname,filt,len(master))
    np.savetxt(workDir+outName,outArr, header=header, fmt=form)


    return None


def pullMags(targname,filt,dir='./',suffix='_0.dat'):

    jdanUse = getJdan(targname,filt)

    master = np.genfromtxt(dir+'master_ids_'+targname+'_'+filt+suffix,names=True)
    masterCat = np.loadtxt(dir+'master_ids_'+targname+'_'+filt+suffix)

    colNs = np.array(master.dtype.names)

    ra_id = np.int(np.where(colNs=='RA')[0])
    dec_id = np.int(np.where(colNs=='DEC')[0])
    flu_id = np.int(np.where(colNs=='flux')[0])
    fla_id = np.int(np.where(colNs=='flags')[0])
    cs_id = np.int(np.where(colNs=='c_star')[0])
    magr = np.int(np.where(colNs=='magr')[0])

    xr = np.int(np.where(colNs=='xr')[0])
    yr = np.int(np.where(colNs=='yr')[0])
    xc = np.int(np.where(colNs=='xc')[0])
    yc = np.int(np.where(colNs=='yc')[0])

    id2 = np.int(np.where(colNs=='id2')[0])
    id3 = np.int(np.where(colNs=='id3')[0])
    id4 = np.int(np.where(colNs=='id4')[0])
    # xt, yt are xo,yo in dithers 2-4 as the transformed positions
    # don't change for the first dither
    xt = np.int(np.where(colNs=='xt')[0])
    yt = np.int(np.where(colNs=='yt')[0])

    id = np.int(np.where(colNs=='id')[0])
    coordRows = masterCat[:,[ra_id,dec_id,flu_id,fla_id,cs_id]]

    nCo = len(jdanUse)*int(9) # 4 is number of dithers
    newCols = np.zeros((len(coordRows), nCo))

    # rowsMast = np.transpose(masterCat)

    jj = 0
    cc = 0
    while jj < len(jdanUse):
        suffix = '_oc.dat'
        cat = np.genfromtxt(dir+jdanUse[jj]+"_"+targname+"_"+filt+suffix,names=True)
        catCat = np.loadtxt(dir+jdanUse[jj]+"_"+targname+"_"+filt+suffix)

        if jj==0:
            idcol = id
        elif jj==1:
            idcol = id2
        elif jj==2:
            idcol = id3
        elif jj==3:
            idcol = id4

        newIDcol = masterCat[:,idcol]
        idx = np.asarray(newIDcol,int)

        reg = catCat[idx]

        newCols[:,cc] = reg[:,magr]
        newCols[:,cc+jj+4] = reg[:,ra_id]
        newCols[:,cc+jj+5] = reg[:,dec_id]

        newCols[:,cc+jj+12] = reg[:,xr]
        newCols[:,cc+jj+13] = reg[:,yr]

        newCols[:,cc+jj+20] = reg[:,xc]
        newCols[:,cc+jj+21] = reg[:,yc]

        newCols[:,cc+jj+28] = reg[:,xt]
        newCols[:,cc+jj+29] = reg[:,yt]

        cc += 1
        jj += 1


    magList = np.hstack((coordRows, newCols))

    header = 'RA DEC flux flags c_star mag1 mag2 mag3 mag4 ra1 '
    header += 'dec1 ra2 dec2 ra3 dec3 ra4 dec4 xr1 yr1 xr2 yr2 xr3 yr3 xr4 yr4 '
    header += 'xc1 yc1 xc2 yc2 xc3 yc3 xc4 yc4 xt1 yt1 xt2 yt2 xt3 yt3 xt4 yt4'

    form = '%1.7f %1.7f %1.4f %d %1.3f %1.4f %1.4f %1.4f %1.4f '
    form +='%1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.4f %1.4f '
    form +='%1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f '
    form +='%1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f '
    form +='%1.4f %1.4f'

    np.savetxt(dir+'matched_w_MagsPos_0.dat',magList,header=header,fmt=form)

    return None


def wrapped(targname,filt):
    seDir, magCatDir, catDir = f2mag_dirs(targname,date='1305',workDir='./')
    # distCor(targname,filt,workDir=catDir)
    # offCor(targname,filt,workDir=catDir)
    # matchWJCs(targname,filt,workDir=catDir,matchtol=3)
    pullMags(targname,filt,dir=catDir,suffix='_0.dat')

    return None
    #
