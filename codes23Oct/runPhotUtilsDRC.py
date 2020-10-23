""" A more general photutils run on DRC files """
# f2mag_dirs and runPhotUtils functions

import numpy as np
import os

from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils import aperture_photometry,CircularAnnulus,CircularAperture
from photutils import DAOStarFinder

# IMPORTANT VARIABLES FOR THIS PROCESS
work_dir = '../'  # this goes to photRun0520
drcDir = '/Volumes/Spare Data/Hannah_Data/origDRCs/'
targFile = work_dir + 'targnamesDirections2.txt'
dateDef = '23Oct'
drcInfoFile = '/Volumes/Spare Data/Hannah_Data/' + "drcTargInfo_new.dat"
suffix_ = '_pu.dat'
radius_ = int(4)

# def main():


def f2mag_dirs(targname,date=dateDef,workDir='./'):

    """
    Makes the ultimate directory structure for the run
    One large directory with the date attached; and
    Sub-directories within it to specify targets
    Returns the targname specific directory
    """

    magCatDir = workDir + '/' + 'drcPhot' + date + '/'
    catDir = magCatDir + 'catDir_' + targname + '/'

    if not os.path.exists(os.path.join(".",magCatDir)):
        os.makedirs(magCatDir)
    if not os.path.exists(os.path.join(".",catDir)):
        os.makedirs(catDir)

    return catDir


def runPhotUtils(drcInfo,radius=4,suffix='_photU.dat'):

    """
    Input:
    drcInfo: a text file with the information from the headers
    of the fits files -- TARGNAME, FILTER1, FILTER2, EXPTIME,
    ORIENTAT, RA, DEC, and JDAN; these can be easily extracted
    using astropy.io.fits; one could also open the fits files
    in this code, but that seems more memory intensive than
    just opening the fits files once and outputting to a file.

    Variables to change: filternames, EEBand, ZPT, r_in,
    and r_out. Can replace _rad with _r(integer radius) if it
    helps you keep track of things.

    When running this in a loop on multiple targets, sometimes
    one could run out of memory space. This causes the computer
    to kill the program. When this happens, just remove the
    targets that have already been run from the drcInfo and
    run again.
    """

    info = np.loadtxt(drcInfo,dtype=str)
    infoN = np.genfromtxt(drcInfo,dtype=str,names=True)
    nameCols = np.array(infoN.dtype.names)

    jdan = np.int(np.where(nameCols=='JDAN')[0])
    filt1 = np.int(np.where(nameCols=='FILTER1')[0])
    filt2 = np.int(np.where(nameCols=='FILTER2')[0])
    targN = np.int(np.where(nameCols=='TARGNAME')[0])

    fileNames = info[:,jdan]

    for ff in range(len(info)):

        image = drcDir + fileNames[ff] + ".fits"
        print(image)

        hdu = fits.open(image)
        sci = hdu[1].data
        hdu.close()

        data = sci.copy()

        f1 = info[:,filt1][ff]
        f2 = info[:,filt2][ff]

        targname = info[:,targN][ff]
        print(targname)

        # Would need to change the below numbers if
        # the data is in different filters. It could
        # be handy to have a table to call.
        if (f1=='F606W') or (f2=='F606W'):
            filt = 'F606W'
            if abs(radius - 4) <= 1e-3:
                EEband = 0.839  # 4 pixel
            elif abs(radius - 3) <= 1e-3:
                EEband = 0.795
            ZPT = 26.667

        elif (f1=='F814W') or (f2=='F814W'):
            filt = 'F814W'
            if abs(radius - 4) <= 1e-3:
                EEband = 0.830  # 4 pixels
            elif abs(radius - 3) <= 1e-3:
                EEband = 0.77
            ZPT = 26.779

        mean, median, std = sigma_clipped_stats(data, sigma=3.0,
                                                maxiters=10)

        daofind = DAOStarFinder(fwhm=2.5, threshold=5.*std)
        sources = daofind(data - median)

        loc = np.array([sources['xcentroid'], sources['ycentroid']])
        positions = np.transpose(loc)

        apertures_rad = CircularAperture(positions, r=radius)
        rawflux_rad = aperture_photometry(data, apertures_rad)

        annulus_apertures = CircularAnnulus(positions, r_in=9.,
                                            r_out=12.)

        annulus_masks = annulus_apertures.to_mask(method='center')

        bkg_median = []
        for mask in annulus_masks:

            annulus_data = mask.multiply(data)
            annulus_data_1d = annulus_data[mask.data > 0]
            _, median_sigclip, _ = sigma_clipped_stats(annulus_data_1d)
            bkg_median.append(median_sigclip)

        bkg_median = np.array(bkg_median)

        rawflux_rad['annulus_median'] = bkg_median
        rawflux_rad['aper_bkg'] = bkg_median * apertures_rad.area

        rawflux_rad['final_phot'] = rawflux_rad['aperture_sum'] \
            - rawflux_rad['aper_bkg']

        mask_negative = (rawflux_rad['final_phot'] > 0)
        rawflux_pos_rad = rawflux_rad[mask_negative]

        final_phot = -2.5 * np.log10(rawflux_pos_rad['final_phot']/EEband) \
            + ZPT

        rawflux_pos_rad['magr'] = final_phot

        rawflux_pos_rad['id'] = np.arange(0,len(rawflux_pos_rad),1)

        s0 = ' '
        header = s0.join(rawflux_pos_rad.dtype.names)

        saveDir = f2mag_dirs(targname,date=dateDef,workDir='../')

        outName = saveDir + fileNames[ff] + '_' + filt + suffix

        np.savetxt(outName,rawflux_pos_rad,header=header)

        # An attempt to free up memory; Didn't seem to work?
        rawflux_pos_rad = None
        data = None
        sci = None

        print('Moving On.')

    return None


# if __name__ == '__main__':
#     main()
