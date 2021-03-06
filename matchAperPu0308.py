import numpy as np
# import matplotlib.pyplot as plt

def matchApPu(targname,dir='./',matchtol=3):

    puN = np.genfromtxt(dir+'HOROLOGIUM-I_filtMatch_pU.dat',names=True)
    pu = np.genfromtxt(dir+'HOROLOGIUM-I_filtMatch_pU.dat')

    aperN = np.genfromtxt(dir+'HOROLOGIUM-I_puTrans_pU.dat',names=True)
    aper = np.genfromtxt(dir+'HOROLOGIUM-I_puTrans_pU.dat')

    id_pu = np.zeros((len(puN),1))
    id_pu[:,0] = np.arange(0,len(puN),1)

    pu = np.hstack((pu,id_pu))
    col_pu = np.array(puN.dtype.names)

    id_ap = np.zeros((len(aperN),1))
    id_ap[:,0] = np.arange(0,len(aperN),1)

    aper = np.hstack((aper,id_ap))
    col_ap = np.array(aperN.dtype.names)

    # Getting columns of x,y of transformed APER to PU
    xA = np.int(np.where(col_ap=='x_puTrans')[0])
    yA = np.int(np.where(col_ap=='y_puTrans')[0])
    idA = len(col_ap)

    xP = np.int(np.where(col_pu=='xcenter_f606w')[0])
    yP = np.int(np.where(col_pu=='ycenter_f606w')[0])
    idP = len(col_pu)

    master_in = pu[:,[xP,yP,idP]]
    x,y,idP_mas = 0,1,2

    cat = aper
    matchids = np.zeros((len(master_in),1))

    nF_out = True
    matchtol=matchtol

    len_pu = len(pu)
    len_ap = len(aper)

    minLen = np.min([len_pu,len_ap])

    while nF_out:

        master, matchids = matchlistID(master_in,cat,matchtol,x,y,xA,yA,idA)

        if len(master)>=int(0.75*minLen):
            nF_out = False
            print('Minimum Number Reached: %d' % len(master),targname)

        else:
            print('Need More Stars')
            print("Pixel Tolerance: %d, Number Stars: %d" % (matchtol,len(master)))
            matchtol += 1
            if matchtol <= 10:
                master_in = pu[:,[xP,yP,idP]]
                matchids = np.zeros((len(master_in),1))
            else:
                print("Sacrificing number of stars for quality of matches.")
                nF_out = False

    master = np.hstack((master,matchids))
    print(targname, len(master)/minLen)

    xP_mas, yP_mas, idP_mas, idA_mas = 0, 1, 2, 3


    idCol_pu = master[:,idP_mas]
    idx_pu = np.asarray(idCol_pu,int)
    reg_pu = pu[idx_pu]

    idCol_ap = master[:,idA_mas]
    idx_ap = np.asarray(idCol_ap,int)
    reg_ap = aper[idx_ap]

    outArr = np.hstack((reg_pu,reg_ap))

    # s0 = ' '
    # header1 = s0.join(col_pu)
    # header2 = s0.join(col_ap)
    #
    # header = header1 + s0 + header2

    header= 'id_f606w xcenter_f606w ycenter_f606w aperture_sum_f606w annulus_median_f606w aper_bkg_f606w final_phot_f606w magr_f606w idNew_f606w id_f814w xcenter_f814w ycenter_f814w aperture_sum_f814w annulus_median_f814w aper_bkg_f814w final_phot_f814w magr_f814w x_f606wTrans y_f606wTrans idNew_f814w id_pu x y m606c m814c nstar sat606 sat814 camera m606 s606 q606 o606 f606 g606 rxs606 sky606 rmssky606 m814 s814 q814 o814 f814 g814 rxs814 sky814 rmssky814 ra dec x_puTrans y_puTrans id_ap'

    np.savetxt(dir+targname+'_aperPuMatch_pU.dat',outArr,header=header)


    return None

def matchlistID(master,cat,matchtol,x1,y1,x2,y2,id_mat):

    matchids_in = np.zeros((len(master),1))

    nF = True
    row = 0

    while nF:

        matchrows = cat[(abs(master[row][x1] - cat[:,x2]) \
            <= matchtol) & (abs(master[row][y1] - cat[:,y2])<= matchtol)]

        if (len(matchrows) == 1):
            matchids_in[row][0] = matchrows[0][id_mat]
            row += 1

        elif (len(matchrows) > 1):
            distDiff = np.zeros((len(matchrows),1))
            for dd in range(len(matchrows)):
                distDiff[dd] = np.sqrt( (master[row][x1] - \
                matchrows[dd][x2])**2 +  (master[row][y1] \
                                    - matchrows[dd][y2])**2)
            small = np.argmin(distDiff)
            matchids_in[row][0] = matchrows[small][id_mat]
            row += 1

        else:
            master = np.delete(master,row,0)
            matchids_in = np.delete(matchids_in,row,0)

        if (row >= len(master)):
            u, udx = np.unique(matchids_in,return_index=True)

            if len(udx)<len(master):
                master = master[udx]
                matchids_in = matchids_in[udx]
                nF = False

            elif len(udx)==len(master):
                nF = False


    return master,matchids_in

#
matchApPu('HOROLOGIUM-I',dir='photUtils0820/',matchtol=3)
