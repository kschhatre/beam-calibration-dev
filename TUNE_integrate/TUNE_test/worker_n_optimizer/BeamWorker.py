
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

import sys
sys.path.insert(1, '/home/berkeleylab/Misc_code/HpBandSter/hpbandster')

from core.worker import Worker

import psutil
import threading


class BeamWorker(Worker):
   

    def __init__(self, *args,sleep_interval=0, **kwargs):
        super().__init__(*args,**kwargs)
        self.sleep_interval = sleep_interval

    def compute(self, config, budget, **kwargs):


        ###########################################
        '''
        INFO about config_id:
             a triplet of ints that uniquely identifies a configuration. the convention is 
             id = (iteration, budget index, running index) with the following meaning:  
                - iteration: the iteration of the optimization algorithms. E.g, for Hyperband that is one round of Successive Halving  
                - budget index: the budget (of the current iteration) for which this configuration was sampled by the optimizer. 
                    This is only nonzero if the majority of the runs fail and Hyperband resamples to fill empty slots, or you use a more ‘advanced’ optimizer. 
                - running index: this is simply an int >= 0 that sort the configs into the order they where sampled, i.e. (x,x,0) was sampled before (x,x,1).

        '''
        ###########################################

        ##### TODO_1: extract the config_id from bohb.run part in the jupyter notebook
        ###### TODO_2: check hpbandster example 3 to understand the way multi proc and example 4 to see how cluster is implemented

        
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
            
            subprocess.call([Repo+'run_process.sh'])

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
        acc = (df.iloc[0] - df.iloc[-1]).abs().sum()
        remains = float(acc)
        #print(acc)

        '''
        ##############################################################################

        # Intermediate iteration stopping
        df1 = pd.read_csv(latest_subdir+"/referenceRealizedModeChoice.csv").iloc[[0, 3]].drop(['iterations'], axis=1)
        extrapolated_coeff = {'bike':0,'car':-2,'cav':2,'drive_transit':0,'ride_hail':-4.5, 'ride_hail_pooled':0,'ride_hail_transit':0, 'walk':4, 'walk_transit':1.5}
        df1 = df1.append(extrapolated_coeff, ignore_index=True)
        df1.loc['3'] = df1.iloc[1:3].sum()
        diff = (df1.iloc[0] - df1.iloc[-1]).abs().sum()
        remains1 = float(diff)

        import core.result as hpres
        log_inf = hpres.logged_results_to_HBS_result('/home/berkeleylab/Calib_documentation/TUNE_integrate/TUNE_test/worker_n_optimizer/')
        all_runs = log_inf.get_all_runs()
        jobid_val = all_runs[-1]['config_id']

       
        if diff < 120:

            thread_to_retain = threading.get_ident()

            
            #with open('pid_list_retain.txt', 'a') as pid_r_file:
                #pid_r_file.write(str(id_to_retain)+'\n')
                
            

            print('Error is below threshold of ',str(diff),' at jobid ', str(jobid_val), ' on thread ',str(thread_to_retain))
            
        else:
            
            thread_to_kill = threading.get_ident()
            
            
            

            #with open('pid_list_kill.txt', 'a') as pid_file:
                #pid_file.write(str(id_to_kill)+'\n')

            try:
                os.kill(id_to_kill, 0)
                p.kill()
                print("Was forced kill")
            except OSError as e:
                print("Was terminated easily")   
                
            p = psutil.Process(id_to_kill)
            p.suspend()         
                       

            print('Error is above threshold (120) and difference is ',str(diff),' for jobid ',str(jobid_val),'Worst performing config from extrapolated prediction is with thread identification ',str(thread_to_kill))
            

        
        ################################################################################  
        '''                  
                
        return({'loss':remains,'info':remains}) 

       


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
    
