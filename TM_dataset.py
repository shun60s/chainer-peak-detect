#coding:utf-8

#
# Chainerで学習できるようにデータを整える。
#


import chainer
import numpy as np
import sys
from rw_dataset import *

class TM_DatsSet(chainer.dataset.DatasetMixin):

	def __init__(self, delta_w, delta_a, CNN=False):
		
		self.f_peak_list, self.amps, self.suffix_list= load_dataset(delta_W=delta_w, delta_A=delta_a)
		self.len=self.f_peak_list.shape[0]
		self.size=self.amps.shape[1]
		self.n_out=1  #　左端の第１ピークの位置を当てるケースを考える。
		self.CNN=CNN
		if self.CNN:
			self.suffix_list = self.suffix_list + '_CNN'
		else:
			self.suffix_list = self.suffix_list + '_MLP'
		
		# normalize:  value to 0-1 
		min = np.min( self.amps)
		max = np.max( self.amps)
		self.amps= (self.amps-min)/(max-min)
		
	def __len__(self):
		return self.len
		
	def get_example(self, i):
		if self.CNN :
			# reshape：1Dデータを 2D-colorの形式に変換
			return self.amps[i].reshape(1,self.size,1) , [self.f_peak_list[i][0]]
		else:
			return self.amps[i] , [self.f_peak_list[i][0]]

if __name__ == '__main__':
	
	f_peak_list_name='dataset/f_peak_list_delta_1_0.npy'
	amps_name='dataset/amps_delta_1_0.npy'
	tm0=TM_DatsSet(f_peak_list_name, amps_name)
	print( tm0.__len__())
	print( tm0.size )
	print( tm0.get_example(1))


#This file uses TAB
