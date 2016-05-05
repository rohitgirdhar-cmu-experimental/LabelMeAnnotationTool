from xml.etree.ElementTree import Element, SubElement, tostring
import os
import h5py
import subprocess
import scipy.misc
import numpy as np
from utils import genXML, genConcatImg

inpath = 'select_res.txt'
trainH5 = '002_HIMYMData_clust50.h5_2'
labelmedir = '/mnt/colossus/Work/public_html/Work/Projects/0006_Affordances/0012_PoseLabelTool/LabelMeAnnotationTool/'
collectionName = 'himym'
himymdir = '/mnt/colossus/Work/public_html/Work/Datasets/0006_TVShows/Data/frames/004_HIMYMFull/'

imOutdir = os.path.join(labelmedir, 'Images/', collectionName); subprocess.call('mkdir -p ' + imOutdir, shell=True)
annotOutdir = os.path.join(labelmedir, 'Annotations/', collectionName); subprocess.call('mkdir -p ' + annotOutdir, shell=True)
listOutpath = os.path.join(labelmedir, 'annotationCache/DirLists/', collectionName + '.txt')

def genFromTxt():
  with open(inpath, 'r') as f:
    for lno,line in enumerate(f.read().splitlines()):
      elts = line.split()
      pose = elts[1:]
      with open(os.path.join(outdir, str(lno+1) + '.xml'), 'w') as fout:
        fout.write(genXML(pose, str(lno+1) + '.jpg', collectionName))

def genFromH5():
  with open(trainH5 + '.imlist', 'r') as f:
    imgslist = f.read().splitlines()
  with open(trainH5 + '.mlist', 'r') as f:
    mlist = f.read().splitlines()
  with h5py.File(trainH5, 'r') as f, open(listOutpath, 'w') as lstOut:
    for imid,imname in enumerate(imgslist):
      out_imname = '%08d' % (imid + 1)
      I = genConcatImg(os.path.join(himymdir, imname), os.path.join(himymdir, mlist[imid]), os.path.join(imOutdir, out_imname + '.jpg'))
      pose = f['pose-label/' + str(imid+1)].value.transpose()
      if pose.ndim == 2:
        poses = pose.reshape((1,-1)).tolist()
      elif pose.ndim == 3:
        poses = []
        for pid in range(pose.shape[2]):
          poses += pose[..., pid].reshape((1,-1)).tolist()
      xml = genXML(poses, out_imname + '.jpg', collectionName)
      with open(os.path.join(annotOutdir, out_imname + '.xml'), 'w') as fout:
        fout.write(xml)
      lstOut.write('%s,%s\n' % (collectionName, out_imname + '.jpg'))

if __name__ == '__main__':
  genFromH5()
