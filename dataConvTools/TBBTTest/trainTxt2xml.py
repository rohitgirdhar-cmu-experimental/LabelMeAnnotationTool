from xml.etree.ElementTree import Element, SubElement, tostring
import os
import h5py
import subprocess
import scipy.misc
import numpy as np
import sys
sys.path.append('..')
from utils import genXML

inpath = 'test_set.txt'
outdir = 'LabelMeLabels/'
imoutdir = 'Images/'
imgsdir = '/mnt/colossus/Work/public_html/Work/Datasets/0006_TVShows/Data/frames/005_TBBT/'

def genFromTxt():
  with open(inpath, 'r') as f:
    for lno,line in enumerate(f.read().splitlines()):
      elts = line.split()
      subprocess.call('cp ' + imgsdir + '/' + elts[0] + ' ' + imoutdir + '/' + str(lno+1) + '.jpg', shell=True)
      pose = [elts[1:35]]
      with open(os.path.join(outdir, str(lno+1) + '.xml'), 'w') as fout:
        fout.write(genXML(pose, str(lno+1) + '.jpg', 'example_folder/TBBTTest'))

if __name__ == '__main__':
  genFromTxt()
