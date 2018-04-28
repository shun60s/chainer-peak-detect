#coding:utf-8

#
# make_dataset.pyで作成したデータの保存と読み込み。
#

import os
import sys
import numpy as np


# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 

def load_dataset(delta_W=1.0, delta_A=1.0):
	# set dir name
	dir_name='dataset/'
	# load peak and length/aera(r1) as npy
	d0= str(delta_W)
	if d0.find('.') > -1:
		d0=d0.replace('.','_')
	f_peak_list_name=dir_name + 'f_peak_list_delta_' + d0 +'.npy'
	print ('loading...', f_peak_list_name)
	d1= str(delta_A)
	if d1.find('.') > -1:
		d1=d0.replace('.','_')
	amps_name=dir_name + 'amps_delta_' + d1 + '.npy'
	print ('loading...',amps_name)
	try:
		f_peak_list= np.load(f_peak_list_name).astype('float32')
		amps= np.load(amps_name).astype('float32')
	except:
		print ('error: load_dataset')
		sys.exit()
	
	suffix_list= '_' + str( amps.shape[0]) + '_delta' + d1
	
	return f_peak_list, amps, suffix_list


def save_dataset(f_peak_list, amps, delta_W, delta_A):
	# check if dir exist
	dir_name='dataset/'
	file_path = os.path.dirname(dir_name)
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	
	# save peak and length/aera(r1) as npy
	d0= str(delta_W)
	if d0.find('.') > -1:
		d0=d0.replace('.','_')
	d1= str(delta_A)
	if d1.find('.') > -1:
 		d1=d1.replace('.','_')
	f_peak_list_name= dir_name + 'f_peak_list_delta_' + d0 +'.npy'
	amps_name= dir_name + 'amps_delta_' + d1 + '.npy'
	np.save(f_peak_list_name, f_peak_list)
	np.save(amps_name, amps)
	print('saved file name ', f_peak_list_name, amps_name)

if __name__ == '__main__':
	
	f,a, suffix_list=load_dataset(delta_W=1.0, delta_A=1.0)
	print ('f.shape', f.shape)
	print ('a.shape', a.shape)
	print ('suffix_list', suffix_list)
#This file uses TAB

