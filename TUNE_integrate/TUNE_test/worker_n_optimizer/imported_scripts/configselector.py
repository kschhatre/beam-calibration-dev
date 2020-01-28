import glob
import os
from sys import argv


def configselector():
    workers = 4
    count_dir = '/home/berkeleylab/Misc_code/HpBandSter/hpbandster/core/'
    with open('/home/berkeleylab/Misc_code/HpBandSter/hpbandster/core/count.txt', 'r' ) as f:
        count = f.read()
    count = int(count)
    count = count%workers


    def returnConfFile(count):
        Dir = '/home/berkeleylab/Repository/beam/test/input/beamville/'
        conf_files = [file for file in glob.glob(os.path.join(Dir, 'beam_*.conf'))] 
        name_dir = [] 
        for name in conf_files:
            a = name
            name_dir.append(a)
        current_conf_file = name_dir[count]
        return current_conf_file
        
    
    address = returnConfFile(count)    

    with open( "/home/berkeleylab/Misc_code/HpBandSter/hpbandster/core/count.txt", "w" ) as f:
        f.write(str(count+1))
    
    return address

#workers = argv[1]
#configselector()