from astropy.io import fits
from astropy import wcs
import numpy as np
import os
import time

from hst_func import *
from f2mag import f2mag_dirs
from getJdan import getJdan

upperDir = "/Volumes/Spare Data/Hannah_Data/"
date = '1305'
# seDir, magCatDir, catDir = f2mag_dirs(date,workDir='./')
seDir, magCatDir, catDir = f2mag_dirs(date,workDir='./')

offset = 20.0

def distCor(targname,filt,workDir='./'):

    jdanUse = getJdan(targname,filt)

    for ff in range(len(jdanUse)):
        #Load catalog
        cat = np.genfromtxt(workDir+magCatDir + jdanUse[ff]+'_'+targname+'_'+filt+'_wMag.dat',names=True)
        catCat = np.loadtxt(workDir+magCatDir + jdanUse[ff]+'_'+targname+'_'+filt+'_wMag.dat')
        #Do correction
        cor = acsDistortion(upperDir+'wfc_'+filt,cat['xr'],cat['yr'])
        #Add columns
        cat = np.hstack((catCat,cor))

        header = "flags RA DEC xr yr flux c_star magr id xc yc"
        form = "%d %1.7f %1.7f %1.4f %1.4f %1.4f %1.3f %1.4f %d %1.4f %1.4f"

        np.savetxt(workDir+catDir+jdanUse[ff]+'_'+targname+'_'+filt+'_dc.dat',cat,fmt=form,header=header)

    return None

def offCor(targname,filt,workDir='./'):

    jdanUse = getJdan(targname,filt)

    if filt=='F606W':
        fils = 'f606w/'
    elif filt=='F814W':
        fils = 'f814w/'

    for jj, jdan in enumerate(jdanUse):

        # Load images, retrieve offset info
        tempim = fits.open(workDir+targname+'_'+fils+jdan+"_flc.fits")

        xoff = float(tempim[0].header["POSTARG1"])
        yoff = float(tempim[0].header["POSTARG2"])

        # Load the respective catalog
        cat = np.genfromtxt(workDir+catDir+jdan+"_"+targname+"_"+filt+"_dc.dat",names=True)
        catCat = np.loadtxt(workDir+catDir+jdan+"_"+targname+"_"+filt+"_dc.dat")

        # Create an array for the new values
        newCol = np.zeros((len(cat),2))

        # Apply offsets to columns
        newCol[:,0] = cat['xc'] - (offset * xoff)
        newCol[:,1] = cat['yc'] - (offset * yoff)

        # Combine to single array and save out
        cat = np.hstack((catCat, newCol))

        header = "flags RA DEC xr yr flux c_star magr id xc yc xo yo"
        form = "%d %1.7f %1.7f %1.4f %1.4f %1.4f %1.3f %1.4f %d %1.4f %1.4f %1.4f %1.4f"

        np.savetxt(workDir+catDir+jdan+"_"+targname+"_"+filt+"_oc.dat",cat,header=header,fmt=form)


    return None


def matchWJCs(targname,filt,iter,workDir='./',matchtol=5):

    # xt, yt = 11,12
    # magr,id = 7,8

    jdanUse = getJdan(targname,filt)
    outName = "master_ids_"+targname+"_"+filt+".dat"

    if iter > 0:
        suffix = "_at_{0:d}".format(iter)+".dat"
    else:
        suffix = '_oc.dat'

    master = np.genfromtxt(workDir+catDir+jdanUse[0]+"_"+targname+'_'+filt +suffix,names=True)
    masterCat = np.loadtxt(workDir+catDir+jdanUse[0]+"_"+targname+'_'+filt +suffix)

    colNs = np.array(master.dtype.names)

    if iter > 0:
        xt = np.int(np.where(colNs=='xt')[0])
        yt = np.int(np.where(colNs=='yt')[0])
        xtstr = 'xt'
        ytstr = 'yt'
    else:
        xt = np.int(np.where(colNs=='xo')[0])
        yt = np.int(np.where(colNs=='yo')[0])
        xtstr = 'xo'
        ytstr = 'yo'
    magr = np.int(np.where(colNs=='magr')[0])
    id = np.int(np.where(colNs=='id')[0])
    # Create an array of zeros with columns equal to the number of non-master dithers to store the matching id for each source
    matchids = np.zeros((len(master), (len(jdanUse)-1)))
    master = np.hstack((masterCat, matchids))

    # Loop through other images
    for dd in range(len(jdanUse)-1):
        # Load catalogs
        cat = np.genfromtxt(workDir+catDir+jdanUse[dd+1]+"_"+targname+'_'+filt+suffix,names=True)
        catCat = np.loadtxt(workDir+catDir+jdanUse[dd+1]+"_"+targname+'_'+filt+suffix)

        colCNs = np.array(cat.dtype.names)
        # if iter > 0:
        #     xtC = np.int(np.where(colCNs=='xt')[0])
        #     ytC = np.int(np.where(colCNs=='yt')[0])
        # else:
        #     xtC = np.int(np.where(colCNs=='xo')[0])
        #     ytC = np.int(np.where(colCNs=='yo')[0])

        nF = True
        row = 0

        while (nF): # not finished
            matchrows = cat[(abs(master[row][xt] - cat[xtstr]) <= matchtol) & (abs(master[row][yt] - cat[ytstr]) <= matchtol)]
            # print(master[row][xt])
            # print(cat.shape)
            # print(cat[:,xt])
    #         matchrows = cat[(abs(master[row][xt] - cat[:,xt]) <= matchtol) & (abs(master[row][yt] - cat[:,yt]) <= matchtol)]
    #         # Setting the proper column number to the matching index.
            if (len(matchrows) == 1):
              master[row][xt+dd+2] = matchrows[0][id]
              row = row + 1

            # elif (len(matchrows) > 1):
            #     magDif = np.zeros((len(matchrows),1))
            #     for mm in range(len(matchrows)):
            #         magDif[mm] = master['magr'][row] - matchrows['magr'][mm]
            #         small = np.argmin(magDif)
            #         master[row][xt+dd+2] = matchrows[small][id]
            #     row += 1
            elif (len(matchrows) > 1):
                # print("more than one source")
                # print(len(matchrows))

                magDif = np.zeros((len(matchrows),1))
                for mm in range(len(matchrows)):
                    magDif[mm] = master[row][magr] - matchrows[mm][magr]
                    # dists[mm] = np.sqrt((master[row][xo]-matchrows[mm][xo])**2 + (master[row][yo]-matchrows[mm][yo])**2)
                    small = np.argmin(magDif)
                    master[row][xt+dd+2] = matchrows[small][id]
                row += 1

            else:
              master = np.delete(master, row, 0)

            if (row >= len(master)):
                nF = False

    header =  "flags RA DEC xr yr flux c_star magr id xc yc xt yt id2 id3 id4"
    form = "%d %1.7f %1.7f %1.4f %1.4f %1.4f %1.3f %1.4f %d %1.4f %1.4f %1.4f %1.4f %d %d %d"

    np.savetxt(workDir+catDir+outName,master, header=header, fmt=form)


    return None

def wcsTrans(targname,filt,workDir='./'):

    jdanUse = getJdan(targname,filt)

    if filt=='F606W':
        fils = 'f606w/'
    elif filt=='F814W':
        fils = 'f814w/'

    cat = np.genfromtxt(workDir+catDir+"master_ids_"+targname+"_"+filt+".dat", names=True)
    catCat = np.loadtxt(workDir+catDir+"master_ids_"+targname+"_"+filt+".dat")

    colNs = np.array(cat.dtype.names)

    xc = np.int(np.where(colNs=='xc')[0])
    yc = np.int(np.where(colNs=='yc')[0])

    newCols = np.zeros((len(cat),2))

    image = fits.open(workDir+targname+'_'+fils+jdanUse[0]+"_flc.fits")
    w = wcs.WCS(header=image[1].header,fobj=image)

    # Applied to distortion corrected values
    # Since drawing from file, the "master" is just the first one listed.
    newCols[:,0], newCols[:,1] = w.wcs_pix2world(catCat[:,xc],catCat[:,yc],1)

    image.close()

    cat = np.hstack((catCat, newCols))

    header = "flags RA DEC xr yr flux c_star magr id xc yc xt yt id2 id3 id4 wcsRA wcsDEC"

    form = "%d %1.7f %1.7f %1.4f %1.4f %1.4f %1.3f %1.4f %d %1.4f %1.4f %1.4f %1.4f %d %d %d %1.7f %1.7f"

    np.savetxt(workDir+catDir+targname+'_'+filt+'_coords.dat',cat,header=header, fmt=form)


    return None

#
def pullMags(targname,filt,iter,workDir='./'):

    jdanUse = getJdan(targname,filt)

    master = np.genfromtxt(workDir+catDir+targname+'_'+filt+'_coords.dat',names=True)
    masterCat = np.loadtxt(workDir+catDir+targname+'_'+filt+'_coords.dat')

    colNs = np.array(master.dtype.names)

    if iter > 0:
        suffix = "_at_{0:d}".format(iter)+".dat"
    else:
        suffix = '_oc.dat'

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
    xt = np.int(np.where(colNs=='xt')[0])
    yt = np.int(np.where(colNs=='yt')[0])
    wra_id = np.int(np.where(colNs=='wcsRA')[0])
    wdec_id = np.int(np.where(colNs=='wcsDEC')[0])
    id = np.int(np.where(colNs=='id')[0])

    coordRows = masterCat[:,[wra_id,wdec_id,flu_id,fla_id,cs_id,xr,yr,xc,yc,xt,yt]]

    nCo = len(jdanUse)*int(3)
    newCols = np.zeros((len(coordRows), nCo))

    jj = 0
    cc = 0
    while cc < len(jdanUse):
        cat = np.genfromtxt(workDir+catDir+jdanUse[jj]+"_"+targname+"_"+filt+suffix,names=True)
        catCat = np.loadtxt(workDir+catDir+jdanUse[jj]+"_"+targname+"_"+filt+suffix)

        if jj==0:
            idcol = id
        else:
            idcol = xt+jj+1

        rowsMast = np.transpose(masterCat)

        newIDcol = rowsMast[idcol]
        idx = np.asarray(newIDcol,int)

        reg = catCat[idx]

        # print(reg.shape)

        newCols[:,cc] = reg[:,magr]
        newCols[:,cc+jj+4] = reg[:,ra_id]
        newCols[:,cc+jj+5] = reg[:,dec_id]


        cc += 1
        jj += 1


    magList = np.hstack((coordRows, newCols))

    header = 'wcsRA wcsDEC flux flags c_star xr yr xc yc xt yt mag1 mag2 mag3 mag4 ra1 dec1 ra2 dec2 ra3 dec3 ra4 dec4'
    form = '%1.7f %1.7f %1.4f %d %1.3f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f %1.7f'

    np.savetxt(workDir+catDir+targname+'_'+filt+'_magList.dat',magList,header=header, fmt=form)


    return None


# def pullRawPos(targname,filt,iter):
#     jdanUse = getJdan(targname,filter)
#
#     master = np.genfromtxt(workDir+catDir+targname+'_'+filt+'_coords.dat',names=True)
#     masterCat = np.loadtxt(workDir+catDir+targname+'_'+filt+'_coords.dat')
#
#     colNs = np.array(master.dtype.names)
#
#     if iter > 0:
#         suffix = "_at_{0:d}".format(iter)+".dat"
#     else:
#         suffix = '_oc.dat'
#
#
#
#     return None

def wrapAll(targname,filt,date,workDir='./',matchtol=5,iter=0):

    distCor(targname,filt,workDir=workDir)
    offCor(targname,filt,workDir=workDir)
    matchWJCs(targname,filt,iter,workDir=workDir,matchtol=matchtol)
    wcsTrans(targname,filt,workDir=workDir)
    pullMags(targname,filt,iter,workDir)

    return None
