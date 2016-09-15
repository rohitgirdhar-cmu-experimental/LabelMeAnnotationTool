import os
labelfiles = ['/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/Fixed/001_HIMYM.txt',
    '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/Fixed/002_HIMYM_traj.txt']
imgsdirs = ['/nfs.yoda/rgirdhar/Work/Data2/014_TVShows/processed/Data/frames/004_HIMYMFull/', 
    '/nfs/ladoga_no_backups/users/xiaolonw/affordance/frames_prune/']
outfpath = '/home/rgirdhar/Work/Data/014_TVShows/processed/Scratch/004_HIMYMFull/014_ManualFineFix/TrainData/001_HIMYM.txt'
with open(outfpath, 'w') as fout:
  for lid, lfile in enumerate(labelfiles):
    with open(lfile, 'r') as f:
      for line in f:
        elts = line.split()
        nposes = int(elts[-1])
        for pid in range(nposes):
          fout.write('%s %s\n' % (os.path.join(imgsdirs[lid], elts[0]), next(f).strip()))
