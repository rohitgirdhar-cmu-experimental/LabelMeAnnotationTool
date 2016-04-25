from xml.etree.ElementTree import Element, SubElement, tostring
import os
import h5py
import subprocess
import scipy.misc
import numpy as np

inpath = 'select_res.txt'
outdir = 'LabelMeLabels/'
trainH5 = '002_HIMYMData_clust50.h5_2'
imoutdir = 'images/'
himymdir = '/mnt/colossus/Work/public_html/Work/Datasets/0006_TVShows/Data/frames/004_HIMYMFull/'

def genXML(poses, fname, foldname):
  root = Element('annotation')
  fname_el = SubElement(root, 'filename')
  fname_el.text = fname
  foldname_el = SubElement(root, 'folder')
  foldname_el.text = foldname
  for pid, pose in enumerate(poses):
    obj_el = SubElement(root, 'object')
    obj_el_name = SubElement(obj_el, 'name')
    obj_el_name.text = 'Pose' + str(pid)
    obj_el_polygon = SubElement(obj_el, 'polygon')
    obj_el_polygon_uname = SubElement(obj_el_polygon, 'username')
    obj_el_polygon_uname.text = 'temp'
    curpos = 0
    for i in range(17):
      obj_el_polygon_pt = SubElement(obj_el_polygon, 'pt')
      obj_el_polygon_pt_x = SubElement(obj_el_polygon_pt, 'x')
      obj_el_polygon_pt_x.text = str(pose[curpos])
      curpos += 1
      obj_el_polygon_pt_y = SubElement(obj_el_polygon_pt, 'y')
      obj_el_polygon_pt_y.text = str(pose[curpos])
      curpos += 1
  return tostring(root)

def genFromTxt():
  with open(inpath, 'r') as f:
    for lno,line in enumerate(f.read().splitlines()):
      elts = line.split()
      pose = elts[1:]
      with open(os.path.join(outdir, str(lno+1) + '.xml'), 'w') as fout:
        fout.write(genXML(pose, str(lno+1) + '.jpg', 'example_folder'))

def genConcatImg(qpath, mpath, outpath, GAP=5):
  Q = scipy.misc.imread(qpath)
  M = scipy.misc.imread(mpath)
  M = scipy.misc.imresize(M, (Q.shape[1] * 1.0) / M.shape[1])
  R = np.concatenate((Q, np.zeros((GAP,Q.shape[1],Q.shape[2])), M), axis=0)
  scipy.misc.imsave(outpath, R)

def genFromH5():
  with open(trainH5 + '.imlist', 'r') as f:
    imgslist = f.read().splitlines()
  with open(trainH5 + '.mlist', 'r') as f:
    mlist = f.read().splitlines()
  with h5py.File(trainH5, 'r') as f:
    for imid,imname in enumerate(imgslist):
      I = genConcatImg(os.path.join(himymdir, imname), os.path.join(himymdir, mlist[imid]), os.path.join(imoutdir, str(imid+1) + '.jpg'))
      pose = f['pose-label/' + str(imid+1)].value.transpose()
      if pose.ndim == 2:
        poses = pose.reshape((1,-1)).tolist()
      elif pose.ndim == 3:
        poses = []
        for pid in range(pose.shape[2]):
          poses += pose[..., pid].reshape((1,-1)).tolist()
      xml = genXML(poses, str(imid+1) + '.jpg', 'example_folder/himym/')
      with open(os.path.join(outdir, str(imid + 1) + '.xml'), 'w') as fout:
        fout.write(xml)

if __name__ == '__main__':
  genFromH5()
