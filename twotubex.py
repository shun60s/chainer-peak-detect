#coding:utf-8

#
# Two Tube Model, A python Class to calculate frequecny response and procee reflection transmission of resonance tube
#
# 2018/4/18  addition, def peak_detect, def set
# 2018/4/19  addition, def revrese_A_sum


import numpy as np
from matplotlib import pyplot as plt

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 



class Class_TwoTube(object):
	def __init__(self, L1, L2, A1, A2, rg0=0.95, rl0=0.9 ,sampling_rate=48000):
		# initalize Tube length and Tube area
		self.L1= L1 # set list of 1st tube's length by unit is [cm]
		self.L2= L2 # set list of 1st tube's area by unit is [cm^2]
		self.A1= A1 # set list of 2nd tube's length by unit is [cm]
		self.A2= A2 # set list of 2nd tube's area by unit is [cm^2]
		self.C0=35000.0  # speed of sound in air, round 35000 cm/second
		self.sr= sampling_rate
		self.tu1=self.L1 / self.C0   # delay time in 1st tube
		self.tu2=self.L2 / self.C0   # delay time in 2nd tube
		self.r1=( self.A2 - self.A1) / ( self.A2 + self.A1)  # reflection coefficient between 1st tube and 2nd tube
		self.rg0=rg0 # rg is reflection coefficient between glottis and 1st tube
		self.rl0=rl0 # reflection coefficient between 2nd tube and mouth
		REDUCTION_FACTOR=0.98  # amplitude decrease ratio per cm in tube
		self.beta1=np.power(REDUCTION_FACTOR , self.L1)
		self.beta2=np.power(REDUCTION_FACTOR , self.L2)
		
	def fone(self, xw):
		# calculate one point of frequecny response
		yi= 0.5 * ( 1.0 + self.rg0 ) * ( 1.0 + self.r1)  * ( 1.0 + self.rl0 ) * np.exp( -1.0j * ( self.tu1 + self.tu2 ) * xw) * self.beta1 * self.beta2
		yb= 1.0 + self.r1 * self.rg0 *  np.exp( -2.0j * self.tu1 * xw ) * self.beta1  + self.r1 * self.rl0 * np.exp( -2.0j * self.tu2 * xw ) * self.beta2 + self.rl0 * self.rg0 * np.exp( -2.0j * (self.tu1 + self.tu2) * xw ) * self.beta1 * self.beta2
		val= yi/yb
		return np.sqrt(val.real ** 2 + val.imag ** 2)

	def H0(self, freq_low=100, freq_high=5000, Band_num=256):
		# get Log scale frequecny response, from freq_low to freq_high, Band_num points
		amp=[]
		freq=[]
		bands= np.zeros(Band_num+1)
		fcl=freq_low * 1.0    # convert to float
		fch=freq_high * 1.0   # convert to float
		delta1=np.power(fch/fcl, 1.0 / (Band_num)) # Log Scale
		bands[0]=fcl
		#print ("i,band = 0", bands[0])
		for i in range(1, Band_num+1):
			bands[i]= bands[i-1] * delta1
			#print ("i,band =", i, bands[i]) 
		for f in bands:
			amp.append(self.fone(f * 2.0 * np.pi))
			
		self.amp=np.log10(amp) * 20
		self.bands=bands
		return  self.amp, self.bands # = amp value, freq list
		

	def peak_detect(self,f_min=250, max_num_formants=5):
		#   対数スペクトルから
		#   山型（凸）のピークポイントを見つける
		#
		#   入力：
		#         （オプション）最低の周波数
		#         （オプション）検出する個数の上限
		#
		#   出力：ピークの周波数  候補がない場合は 零になっている
		#
		#   条件：　これを呼ぶ前に あらかじめ　H0で対数スペクトルを計算しておくこと。
		#       
		f_peak=np.zeros(max_num_formants)
		f_peak_list=np.ones(max_num_formants) * -1
		c0=0
		for i in range (1,len(self.amp)-1):
			if f_min is not None and  self.bands[i] <= f_min :
				continue
			if self.amp[i] > self.amp[i-1] and self.amp[i] > self.amp[i+1] :
				f_peak[c0]=self.bands[i]
				f_peak_list[c0]=i
				c0+= 1
			if c0 >= max_num_formants:
				break
				
		return f_peak, f_peak_list
		
	def set(self, L1, L2, A1, A2):
		# set Tube length and Tube area
		self.L1= L1 # set list of 1st tube's length by unit is [cm]
		self.L2= L2 # set list of 1st tube's area by unit is [cm^2]
		self.A1= A1 # set list of 2nd tube's length by unit is [cm]
		self.A2= A2 # set list of 2nd tube's area by unit is [cm^2]
		self.tu1=self.L1 / self.C0   # delay time in 1st tube
		self.tu2=self.L2 / self.C0   # delay time in 2nd tube
		self.r1=( self.A2 - self.A1) / ( self.A2 + self.A1)  # reflection coefficient between 1st tube and 2nd tube


	def revrese_A_sum(self, r1, A_sum=8.0):
		# input 
		#       r1  : reflection coefficient between 1st tube and 2nd tube
		#       A_sum = A1 + A2  : sum of 1st and 2nd tube's area by unit is [cm^2]
		# output 
		#       A1, A2
		
		return (1.0 + r1) * A_sum * 0.5, (1.0 - r1) * A_sum * 0.5 
		


def down_sample(amp, bands, NDIM=64):
	amp0=np.zeros(NDIM)
	bands0=np.zeros(NDIM)
	delta= int(len(amp) / NDIM)
	
	print ('len(amp)', len(bands0) )
	for loop in range (NDIM):
		amp0[loop]= np.max(amp[delta * loop :  delta *(loop+1)])
		bands0[loop]= bands[int(delta*loop + delta*0.5)]
		
	return amp0, bands0



if __name__ == '__main__':
	
	# Length & Area value, from problems 3.8 in "Digital Processing of Speech Signals" by L.R.Rabiner and R.W.Schafer
	#
	# /a/
	L1_a=9.0    # set list of 1st tube's length by unit is [cm]
	A1_a=1.0    # set list of 1st tube's area by unit is [cm^2]
	L2_a=8.0    # set list of 2nd tube's length by unit is [cm]
	A2_a=7.0    # set list of 2nd tube's area by unit is [cm^2]
	
	# insatnce
	twotube_a  =  Class_TwoTube(L1_a,L2_a,A1_a,A2_a)
	amp, bands = twotube_a.H0(freq_high=3500, Band_num=64)
	f_peaks, f_peak_list = twotube_a.peak_detect()
	
	print ( f_peaks, f_peak_list )
	
	import matplotlib.pyplot as plt
	
	plt.subplot(2,2,1)
	plt.plot( bands, amp)
	
	plt.tight_layout() 
	plt.show()
	
	
#This file uses TAB

