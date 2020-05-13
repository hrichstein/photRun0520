import numpy as np
import os

upperDir = '/Volumes/Spare Data/Hannah_Data/'

def sex1(image, outfile, expTime,band='F606W') :
  #creates a sextractor line e.g sex img.fits -c default.sex -catalog_name something.txt
  dir = '~/seFilesFLCs/'

  if band=='F606W':
      com = [ "sex ", image, " -c defaultVBand_ACS.sex -GAIN ", str(1./expTime),
      " -CATALOG_NAME ",dir+outfile]

  else:
      com = [ "sex ", image, " -c defaultIBand_ACS.sex -GAIN ", str(1./expTime),
       " -CATALOG_NAME ",dir+outfile]

  s0=''
  com = s0.join(com)

  return com


def makeSex(nameslist,dir=upperDir):

    img_arr = np.genfromtxt(dir+nameslist,usecols=(0,1,4),dtype=str)

    filename =

    if band=='F606W':
        # com_file = open(dir+'F606WcomsList0411.txt','w')

    else:
        # com_file = open(dir+'F814WcomsList0411.txt','w')

    for ii in range(len(img_arr[:,0])):
        img_name = img_arr[:,0][ii]
        obj_name = img_arr[:,1][ii]

        filt1 = img_arr[:,2][ii]
        filt1 = img_arr[:,3][ii]


        img_tag = img_name.replace('_WJC.fits','')
        outfile = 'se_' + img_tag + '_' + str(obj_name) + "_" + band + '.dat'

        expTime_str = img_arr[:,2][ii]

        expTime_fl = np.float(expTime_str)

        # expTime_inv = 1./expTime_fl
        #
        # expTime2_str = (expTime_inv)

        tmpCom = sex1(img_name,outfile,expTime_fl,band)

        com_file.write('%s\n' % tmpCom)

    com_file.close()

    return None
