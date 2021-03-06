import scipy.misc
import numpy as np
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.etree.ElementTree as ET

def genConcatImg(qpath, mpath, outpath, GAP=5):
  Q = scipy.misc.imread(qpath)
  M = scipy.misc.imread(mpath)
  # M = scipy.misc.imresize(M, (Q.shape[1] * 1.0) / M.shape[1])
  M = scipy.misc.imresize(M, (Q.shape[0], Q.shape[1], Q.shape[2])) 

  if Q.shape[0] != M.shape[0] or Q.shape[1] != M.shape[1]: 
    print(qpath)
    print(mpath)

  R = np.concatenate((Q, np.zeros((GAP,Q.shape[1],Q.shape[2])), M), axis=0)
  scipy.misc.imsave(outpath, R)


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

def readXML(fname):
  tree = ET.parse(fname)
  objs = tree.findall('object')
  poses = []
  for obj in objs:
    if obj.find('deleted') is not None and obj.find('deleted').text == '1':
      return None
    polygon = obj.find('polygon')
    pose = []
    for pt in polygon.findall('pt'):
      pose.append(pt.find('x').text)
      pose.append(pt.find('y').text)
    poses.append(pose)
  return poses

