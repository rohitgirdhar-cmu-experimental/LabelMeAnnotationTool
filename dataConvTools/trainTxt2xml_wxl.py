from xml.etree.ElementTree import Element, SubElement, tostring
import os
import h5py
import subprocess
import scipy.misc
import numpy as np
import urllib, cStringIO
import urlparse
from utils import genXML, genConcatImg

if 0:
  inpath = 'pairs_216.txt'
  labelmedir = '/mnt/colossus/Work/public_html/Work/Projects/0006_Affordances/0012_PoseLabelTool/LabelMeAnnotationTool/'
  collectionName = 'himym_traj'
  himymdir = 'http://ladoga.graphics.cs.cmu.edu/xiaolonw/affordance/frames_prune/'
elif 1:
  inpath = 'TBBTData/pairs_TBBT54.txt'
  labelmedir = '/mnt/colossus/Work/public_html/Work/Projects/0006_Affordances/0012_PoseLabelTool/LabelMeAnnotationTool/'
  collectionName = 'tbbt_traj'
  himymdir = 'http://ladoga.graphics.cs.cmu.edu/xiaolonw/affordance_TBBT/frames_prune/'


imOutdir = os.path.join(labelmedir, 'Images/', collectionName); subprocess.call('mkdir -p ' + imOutdir, shell=True)
annotOutdir = os.path.join(labelmedir, 'Annotations/', collectionName); subprocess.call('mkdir -p ' + annotOutdir, shell=True)
listOutpath = os.path.join(labelmedir, 'annotationCache/DirLists/', collectionName + '.txt')

def genFromTxt():
  with open(inpath, 'r') as f, open(listOutpath, 'w') as lstOut:
    for lno,line in enumerate(f):
      elts = line.split()
      out_imname = '%08d' % (lno + 1)
      I = genConcatImg(
        cStringIO.StringIO(urllib.urlopen(urlparse.urljoin(himymdir, elts[0])).read()),
        cStringIO.StringIO(urllib.urlopen(urlparse.urljoin(himymdir, elts[1])).read()),
        os.path.join(imOutdir, out_imname + '.jpg'))
      poses = []
      for pid in range(int(elts[2])):
        poses.append(next(f).split())
        try:
          assert(len(poses[-1]) == 34)
        except:
          import pdb
          pdb.set_trace()
      xml = genXML(poses, out_imname + '.jpg', collectionName)
      with open(os.path.join(annotOutdir, out_imname + '.xml'), 'w') as fout:
        fout.write(xml)
      lstOut.write('%s,%s\n' % (collectionName, out_imname + '.jpg'))

if __name__ == '__main__':
  genFromTxt()
