from xml.etree.ElementTree import Element, SubElement, tostring
import os
import h5py
import subprocess
import scipy.misc
import numpy as np

inpath = 'test_set.txt'
outdir = 'LabelMeLabels/'
imoutdir = 'Images/'
imgsdir = '/mnt/colossus/Work/public_html/Work/Datasets/0006_TVShows/Data/frames/005_TBBT/'

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
      subprocess.call('cp ' + imgsdir + '/' + elts[0] + ' ' + imoutdir + '/' + str(lno+1) + '.jpg', shell=True)
      pose = [elts[1:35]]
      with open(os.path.join(outdir, str(lno+1) + '.xml'), 'w') as fout:
        fout.write(genXML(pose, str(lno+1) + '.jpg', 'example_folder/TBBTTest'))

if __name__ == '__main__':
  genFromTxt()
