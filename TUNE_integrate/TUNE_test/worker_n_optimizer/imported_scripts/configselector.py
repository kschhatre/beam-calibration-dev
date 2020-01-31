import glob
import os
from sys import argv

simulation = 'beamville' 
# 'beamville' or 'urbansim-1k' or 'urbansim-10k'

def configselector():
    workers = 4
    count_dir = '/home/berkeleylab/Misc_code/HpBandSter/hpbandster/core/'
    with open('/home/berkeleylab/Misc_code/HpBandSter/hpbandster/core/count.txt', 'r' ) as f:
        count = f.read()
    count = int(count)
    count = count%workers


    def returnConfFile(count):
        
        if simulation == 'beamville':
            Dir = '/home/berkeleylab/Repository/beam/test/input/'+simulation+'/'+simulation[:4] 
        else:
            Dir = '/home/berkeleylab/Repository/beam/test/input/sf-light/'+simulation

        conf_files = [file for file in glob.glob(os.path.join(Dir+'_*.conf'))] 
        name_dir = [] 
        for name in conf_files:
            name_dir.append(name)
        current_conf_file = name_dir[count]
        return current_conf_file
        
    
    address = returnConfFile(count)    

    with open( "/home/berkeleylab/Misc_code/HpBandSter/hpbandster/core/count.txt", "w" ) as f:
        f.write(str(count+1))
    
    return address
