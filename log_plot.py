#coding:utf-8

# ディレクトリー名に 'result' が含まれるものから、
# Chainerのlog出力のmain/lossをプロットする。
#

import os
import json
import numpy as np
from matplotlib import pyplot as plt

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 
#  chainer 3.2.0

def load_log( f_dir):
    with open( f_dir+'/log','r') as f:
        data1= json.load(f)
        y1=np.zeros( len(data1))
        x1=np.zeros( len(data1))
        for i in range (len(data1)):
            y1[i]=data1[i]['main/loss']
            x1[i]=data1[i]['epoch']
    return x1,y1


def get_dir_list(path0='./'):
    list0= os.listdir(path0)
    dir_list= [s for s in list0 if 'result' in s]  # 文字列resetを含むディレクトリーを抽出
    comment_list = [s.replace('result_', '') for s in dir_list] # 文字列reset_を空文に変更。残りは作成情報。
    return dir_list, comment_list
    
if __name__ == '__main__':
    
    # 名称に　'result' が含まれる ディレクトリーを探す
    flist, clist= get_dir_list()
    len0=len(flist)
    
    fig = plt.figure()
    # label out of subplot(111)
    a = fig.add_subplot(221)
    a.set_xlabel('epoch')
    a.set_ylabel('main/loss')
    a.set_title('comparison of condition, sample number')
    a.grid()
    plt.yscale('log')
    
    for (f,c) in zip(flist,clist):
        x1,y1=load_log(f)
        print (f,c)
        a.plot(x1, y1, marker='x', label=c, markersize=2)
    
    # label out
    a.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.tight_layout() 
    plt.show()