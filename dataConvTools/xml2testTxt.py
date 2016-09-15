import xml.etree.ElementTree as ET
import os
import h5py
import subprocess
import scipy.misc
import numpy as np
from utils import readXML


def genFromTxt():  # wxl
  with open(inpath, 'r') as f, open(outpath, 'w') as fout:
    for lno,line in enumerate(f):
      out_imname = '%08d' % (lno + 1)
      elts = line.split()
      for j in range(int(elts[-1])):
        next(f)
      poses = readXML(os.path.join(correctedDir, out_imname + '.xml'))
      if poses is None:
        poses = []
      fout.write('%s %s %d\n' % (elts[0], elts[1], len(poses)))
      for pose in poses:
        fout.write('%s\n' % (' '.join(pose)))

def genFromH5():  # rohit
  with open(inpath + '.imlist', 'r') as f:
    imgslist = f.read().splitlines()
  with open(inpath + '.mlist', 'r') as f:
    mlist = f.read().splitlines()
  with h5py.File(inpath, 'r') as f, open(outpath, 'w') as fout:
    for imid,imname in enumerate(imgslist):
      out_imname = '%08d' % (imid + 1)
      poses = readXML(os.path.join(correctedDir, out_imname + '.xml'))
      if poses is None:
          poses = []
      fout.write('%s %s %d\n' % (imname, mlist[imid], len(poses)))
      if poses:
        for pose in poses:
          fout.write('%s\n' % (' '.join(pose)))

if __name__ == '__main__':
  if 0:
    inpath = '/nfs.yoda/rgirdhar/Work/Data2/014_TVShows/processed/Scratch/004_HIMYMFull/011_TrainingData/002_HIMYMData_clust50.h5_2'
    outpath = '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/Fixed/001_HIMYM.txt'
    correctedDir = '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/XML/himym/'
    method = genFromH5
  elif 1:
    inpath = '/nfs/ladoga_no_backups/users/xiaolonw/affordance/pairs_216.txt'
    outpath = '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/Fixed/002_HIMYM_traj.txt'
    correctedDir = '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/XML/himym_traj/'
    method = genFromTxt

  method()
