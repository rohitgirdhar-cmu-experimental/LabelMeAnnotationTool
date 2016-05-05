import xml.etree.ElementTree as ET
import os
import h5py
import subprocess
import scipy.misc
import numpy as np
from utils import readXML

inpath = '/nfs.yoda/rgirdhar/Work/Data2/014_TVShows/processed/Scratch/004_HIMYMFull/011_TrainingData/002_HIMYMData_clust50.h5_2'
outpath = '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/Fixed/001_HIMYM.txt'
correctedDir = '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/XML/himym/'

def genFromTxt():
  with open(inpath, 'r') as f, open(outpath, 'w') as fout:
    for lno,line in enumerate(f.read().splitlines()):
      if lno+1 in cur_labeled:
        elts = line.split()
        pose = readXML(os.path.join(correctedDir, str(lno+1) + '.xml'))
        if pose:
          fout.write('%s %s %s\n' % (elts[0], ' '.join(pose), elts[-1]))

def genFromH5():
  with open(inpath + '.imlist', 'r') as f:
    imgslist = f.read().splitlines()
  with open(inpath + '.mlist', 'r') as f:
    mlist = f.read().splitlines()
  with h5py.File(inpath, 'r') as f, open(outpath, 'w') as fout:
    for imid,imname in enumerate(imgslist):
      out_imname = '%08d' % (imid + 1)
      poses = readXML(os.path.join(correctedDir, out_imname + '.xml'))
      if poses:
        for pose in poses:
          fout.write('%s %s\n' % (imname, ' '.join(pose)))

if __name__ == '__main__':
  genFromH5()
