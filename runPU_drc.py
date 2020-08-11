import numpy as np
import os
from matplotlib import pyplot as plt
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils import aperture_photometry,CircularAnnulus,CircularAperture
from photutils import DAOStarFinder


# Work in progress

drcDir = './hor1DRCs/'

def runPhotUtils(targname,filt,saveDir='./'):

    name =
    
