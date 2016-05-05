import xml.etree.ElementTree as ET
import os
import h5py
import subprocess
import scipy.misc
import numpy as np
import sys
sys.path.append('..')
from utils import readXML

inpath = 'test_set.txt'
labeldir = 'LabelMeLabels/'
outpath = 'test_set_corrected.txt'
imoutdir = 'Images/'
imgsdir = '/mnt/colossus/Work/public_html/Work/Datasets/0006_TVShows/Data/frames/005_TBBT/'
correctedDir = '/mnt/colossus/Work/public_html/Work/Projects/0006_Affordances/0012_PoseLabelTool/LabelMeAnnotationTool/Annotations/example_folder/TBBTTest/'
cur_labeled = range(1, 70+1) + range(94, 130+1) # only these images have been labeled

def genFromTxt():
  with open(inpath, 'r') as f, open(outpath, 'w') as fout:
    for lno,line in enumerate(f.read().splitlines()):
      if lno+1 in cur_labeled:
        elts = line.split()
        pose = readXML(os.path.join(correctedDir, str(lno+1) + '.xml'))[0]
        if pose:
          fout.write('%s %s %s\n' % (elts[0], ' '.join(pose), elts[-1]))

if __name__ == '__main__':
  genFromTxt()
