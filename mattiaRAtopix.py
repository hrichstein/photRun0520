import numpy as np

dir1='/Volumes/Spare Data/Hannah_Data/mattia/rephotometryquestion/'
master = np.genfromtxt(dir1 + 'HOROLOGIUM_CF.1.TOSEND.CAT')

x, y, m606c, m814c, nstar, sat606, sat814, camera, m606, s606, q606, o606, f606, g606, rxs606, sky606, rmssky606, m814, s814, q814, o814, f814, g814, rxs814, sky814, rmssky814, ra, dec = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

ra_arr = [43.8922300,43.9197460,43.9220320,43.8584350,43.8746860,43.8534360]
dec_arr = [-54.1360640,-54.1128260,-54.1165550,-54.1153960,-54.1152020,-54.1320310]

matchPix = np.zeros((len(master),2))

nF = True
row = 0

while (nF): 
    for cc, coord in enumerate(ra_arr):
        matchrows = master[(abs(master[row][ra]) - coord)]
