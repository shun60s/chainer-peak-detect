#coding:utf-8

#
# いくつかの凸型のピークをもつ１Ｄデータを作成する。
# １Ｄデータと　ピークがある位置データ(index)を出力する。
#


import argparse
import os
import numpy as np
from twotubex import *
from rw_dataset import *

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 



def make_dataset(WL_max, WL_min, WM, delta_W, A_max, A_min, delta_A):
	# create an dummy instance 
	twotube  =  Class_TwoTube(9.0,8.0,1.0,7.0)  # dummy value
	
	# compute r1 value and sort out
	r1_list=[]
	for A1 in np.linspace( A_min, A_max, int((A_max - A_min) / delta_A+1)):
		for A2 in np.linspace( A_min, A_max, int((A_max - A_min) / delta_A+1)):	
			r1=(A2 -A1) / (A2 + A1)
			if r1 not in r1_list:
				r1_list.append( r1)
	
	# count all iteration number
	c0=0
	for WL in np.linspace( WL_min, WL_max, int((WL_max - WL_min) / delta_W+1)):
		for L1 in np.linspace(WM,(WL - WM), int((WL - WM)/delta_W + 1)): 
						c0+=len(r1_list)
						
	print ('all iteration number= ',c0)
	
	# prepare output
	max_num_formant=3 #　ピークのある位置検出をする上限数
	band_num=64 #バンド数を64に設定
	f_peaks_list=np.zeros([c0, max_num_formant])
	amps=np.zeros([c0,band_num]) 
	
	
	# get peaks per L1,L2,A1,and A2
	c0=0
	for WL in np.linspace( WL_min, WL_max, int((WL_max - WL_min) / delta_W+1)):
		print ('WL= ',WL)
		for L1 in np.linspace(WM,(WL - WM), int((WL - WM)/delta_W + 1)): 
			L2= WL - L1
			#print ( L1 + L2)
			
			for r1 in r1_list:
				A1, A2 =twotube.revrese_A_sum(r1)
				#print (A1,A2)
				twotube.set(L1,L2,A1,A2)
				amp, bands=twotube.H0(freq_high=5000, Band_num=band_num)
				amps[c0]=amp[0:band_num]
				f_peak, f_peak_list=twotube.peak_detect(max_num_formants=max_num_formant)
				#print (c0, f_peak)
				f_peaks_list[c0]=f_peak_list
				c0+=1  # count up
					
	return f_peaks_list, amps



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='make dataset')
	parser.add_argument('--delta', '-d', type=float, default=1.0, help='delta for length and area')
	args = parser.parse_args()
	delta=args.delta
	# set parameters for train
	WL_max=20     # whole length
	WL_min=10     # whole length
	WM=1.0        # minmum length
	delta_W= delta #0.5  # =1.0 #  compute step
	
	A_max=13.0     # maxmum area
	A_min=1.0      # minmum area
	delta_A= delta  #0.5   # =1.0  # compute step
	
	f_peak_list, amps = make_dataset(WL_max, WL_min, WM, delta_W, A_max, A_min, delta_A)
	
	print ( np.max(amps), np.min(amps))
	
	save_dataset(f_peak_list, amps,  delta_W, delta_A)
	
	

	
#This file uses TAB

