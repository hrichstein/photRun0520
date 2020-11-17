import numpy as np
# import os


def outputEl(targname,dir='./'):

    # x = os.listdir(dir)
    # for ii in x:
    #     if ii.endswith('_fullCat_ALL.dat'):
    #         file = ii
    #     elif ii.endswith('_fullCat.dat'):
    #         file = ii
    file = targname + '_fullCat.dat'

    fileN = np.genfromtxt(dir + file,names=True)
    file = np.genfromtxt(dir + file)

    colNs = np.array(fileN.dtype.names)

    x_f606w = np.int(np.where(colNs=='xcenter_f606w')[0])
    y_f606w = np.int(np.where(colNs=='ycenter_f606w')[0])

    x_f814w = np.int(np.where(colNs=='xcenter_f814w')[0])
    y_f814w = np.int(np.where(colNs=='ycenter_f814w')[0])

    magr_f606w = np.int(np.where(colNs=='magr_f606w')[0])
    magr_f814w = np.int(np.where(colNs=='magr_f814w')[0])

    mean_f606w = np.int(np.where(colNs=='mean_f606w')[0])
    mean_f814w = np.int(np.where(colNs=='mean_f814w')[0])

    err_f606w = np.int(np.where(colNs=='stdev_f606w')[0])
    err_f814w = np.int(np.where(colNs=='stdev_f814w')[0])

    flag_f606w = np.int(np.where(colNs=='six_4_flag_f606w')[0])
    flag_f814w = np.int(np.where(colNs=='six_4_flag_f814w')[0])

    outArr = file[:,[x_f606w,y_f606w,magr_f606w,mean_f606w,err_f606w,
                     flag_f606w,x_f814w,y_f814w,magr_f814w,mean_f814w,
                     err_f814w,flag_f814w]]

    header = 'x_f606w y_f606w magr_f606w flcMag_f606w err_f606w star_f606w'
    header += ' x_f814w y_f814w magr_f814w flcMag_f814w err_f814w star_f814w'

    np.savetxt('../forElena16Nov/' + targname + '_cat16Nov.dat',outArr,
               header=header)

    return None

#
