
import time
import os
import pandas as pd
import numpy as np
import glob
import itertools 
import subprocess
import math

import ConfigSpace as CS 
import ConfigSpace.hyperparameters as CSH
from hpbandster.core.worker import Worker


class BeamWorker(Worker):
   

    def __init__(self, *args,sleep_interval=0, **kwargs):
        super().__init__(*args,**kwargs)
        self.sleep_interval = sleep_interval

    def compute(self, config, budget, **kwargs):
        
        Repo='/home/berkeleylab/Repository/beam/'
        Current='/home/berkeleylab/Calib_documentation/TUNE_integrate/TUNE_test'


        def ext_change(param):
            if param == 'edit':
                for filename in glob.iglob(os.path.join(Repo, 'test/input/beamville/beam.conf')):
                    os.rename(filename, filename[:-9] + 'beam.txt')
            elif param == 'save':
                for filename in glob.iglob(os.path.join(Repo, 'test/input/beamville/beam.txt')):
                    os.rename(filename, filename[:-8] + 'beam.conf')
                    
        ext_change('edit')
                    
        def change_conf(config):
            with open(Repo+'test/input/beamville/beam.txt', 'r') as fin:
                file_text=fin.readlines()
                
            for i in range(25,33,1):                
                file_text[i] = file_text[i].split('=',1)[0]+'= '
    
            file_text[25] = file_text[25]+str(config['car_intercept'])
            file_text[26] = file_text[26]+str(config['walk_transit_intercept'])
            file_text[27] = file_text[27]+str(config['drive_transit_intercept'])
            file_text[28] = file_text[28]+str(config['ride_hail_transit_intercept'])
            file_text[29] = file_text[29]+str(config['ride_hail_intercept'])
            file_text[30] = file_text[30]+str(config['ride_hail_pooled_intercept'])
            file_text[31] = file_text[31]+str(config['walk_intercept'])
            file_text[32] = file_text[32]+str(config['bike_intercept'])
            
            for j in range(25,33,1):
                file_text[j] = file_text[j]+' \n'
                
            with open(Repo+'test/input/beamville/beam.txt', 'w') as fini:
                for i in file_text:
                    fini.write(i)
                    
        change_conf(config)            
    
        ext_change('save')
                    
        def run_beam():
            os.chdir(Repo)
            subprocess.call([Repo+'runme.sh'])
            os.chdir(Current)
            
        run_beam()
            
        def all_subdirs_of(b='/home/berkeleylab/Repository/beam/output/beamville/'):
            result = []
            for d in os.listdir(b):
                bd = os.path.join(b, d)
                if os.path.isdir(bd): result.append(bd)
            return result
        
        latest_subdir = max(all_subdirs_of(), key=os.path.getmtime)
        df = pd.read_csv(latest_subdir+"/referenceRealizedModeChoice.csv").iloc[[0, -1]].drop(['iterations'], axis=1)
        acc = (df.iloc[0] - df.iloc[-1]).abs().sum()/df.iloc[0].sum()
        remains = float(1-acc)
        
        print(acc)
    
        return({'loss':float(remains),'info':remains})

        # check keras example
        # add tag for iteration number and check corresponding column inmode choice csv file
    
    
    
    

    @staticmethod
    def get_configspace():
        cs = CS.ConfigurationSpace()
        
        '''
        HYPERPARAMETERS:

        +-------------------------+----------------+-----------------+------------------------+
        | Parameter Name          | Parameter type |  Range/Choices  | Comment                |
        +=========================+================+=================+========================+
        | car_intercept           |  float         | [-5 , 10   ]    | standard continuous    |
        |                         |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        | walk_transit_intercept  |  float         | [-5 , 10   ]    | standard continuous    |
        |                         |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        | drive_transit_intercept |  float         | [-5 , 10   ]    | standard continuous    |
        |                         |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        | ride_hail_transit_      |  float         | [-5 , 10   ]    | standard continuous    |
        | intercept               |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        | ride_hail_intercept     |  float         | [-5 , 10   ]    | standard continuous    |
        |                         |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        | ride_hail_pooled_       |  float         | [-5 , 10   ]    | standard continuous    |
        | intercept               |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        | walk_intercept          |  float         | [-5 , 10   ]    | standard continuous    |
        |                         |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        | bike_intercept          |  float         | [-5 , 10   ]    | standard continuous    |
        |                         |                |                 | parameter              |
        +-------------------------+----------------+-----------------+------------------------+
        
        '''
        
        car_intercept = CSH.UniformFloatHyperparameter('car_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        walk_transit_intercept = CSH.UniformFloatHyperparameter('walk_transit_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        drive_transit_intercept = CSH.UniformFloatHyperparameter('drive_transit_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        ride_hail_transit_intercept = CSH.UniformFloatHyperparameter('ride_hail_transit_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        ride_hail_intercept = CSH.UniformFloatHyperparameter('ride_hail_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        ride_hail_pooled_intercept = CSH.UniformFloatHyperparameter('ride_hail_pooled_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        walk_intercept = CSH.UniformFloatHyperparameter('walk_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        bike_intercept = CSH.UniformFloatHyperparameter('bike_intercept', lower=-5.0, upper=10.0,default_value=1.0,log=False)
        
        cs.add_hyperparameters([car_intercept,walk_transit_intercept,drive_transit_intercept,ride_hail_transit_intercept,ride_hail_intercept,ride_hail_pooled_intercept,walk_intercept,bike_intercept])
        
        return cs
    
