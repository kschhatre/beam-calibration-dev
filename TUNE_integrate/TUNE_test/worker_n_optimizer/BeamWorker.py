
import time, os, glob, itertools, subprocess, math, sys, psutil, threading
import pandas as pd
import numpy as np
import ConfigSpace as CS 
import ConfigSpace.hyperparameters as CSH

sys.path.insert(1, '/home/berkeleylab/Misc_code/HpBandSter/hpbandster')

from core.worker import Worker
from core.configselector import configselector
import core.result as hpres

class BeamWorker(Worker):
   
    def __init__(self, *args,sleep_interval=0, **kwargs):
        super().__init__(*args,**kwargs)
        self.sleep_interval = sleep_interval

    def compute(self, config, budget, **kwargs):

        '''
        INFO about config_id:
             a triplet of ints that uniquely identifies a configuration. the convention is 
             id = (iteration, budget index, running index) with the following meaning:  
                - iteration: the iteration of the optimization algorithms. E.g, for Hyperband that is one round of Successive Halving  
                - budget index: the budget (of the current iteration) for which this configuration was sampled by the optimizer. 
                    This is only nonzero if the majority of the runs fail and Hyperband resamples to fill empty slots, or you use a more ‘advanced’ optimizer. 
                - running index: this is simply an int >= 0 that sort the configs into the order they where sampled, i.e. (x,x,0) was sampled before (x,x,1).

        '''

        ##### TODO_1: extract the config_id from directly from bohb.run part in the jupyter notebook and not from the logger file, its faster
        ###### TODO_2: check hpbandster example 3 to understand the way multi proc and example 4 to see how cluster is implemented

        # sf light on AWS
        # comparison vs nonearly stopping
        
        Repo='/home/berkeleylab/Repository/beam/'
        Current='/home/berkeleylab/Calib_documentation/TUNE_integrate/TUNE_test'
        threshold = 115 # L1 distance
        finaliteration = '10' 

        picked_conf_file = configselector() # External files usage: configselector.py and count.txt from hpbandster/core
        instance_path = picked_conf_file[34:]
        conf_identifier = picked_conf_file[55:-4]

        p = 25 # intercepts
        q = 13 # last iterations
        selected_sim = picked_conf_file[65:][0] 
        if selected_sim == 'f': #beam
            selected_sim = 'beamville'
            p = p-1 
            q = q-3 
        else:
            selected_sim = 'sf-light' # urbansim 1k or 10k
   
        # for logging:
        with open(Repo+"instanceconfpath.txt", "w") as text_file: # external file usage instanceconfpath.txt from beam home
            text_file.write(instance_path) 

        # Pulling conf files from the confselector

        def ext_change(param):
            if param == 'edit':
                os.rename(picked_conf_file, picked_conf_file[:-4] + 'txt')
            elif param == 'save':
                for filename in glob.iglob(os.path.join(Repo, 'test/input/'+selected_sim+'/',conf_identifier+'txt' )):
                    os.rename(filename, filename[:-3] + 'conf')
                                       
        def change_conf(config):

            with open(Repo+'test/input/'+selected_sim+'/'+conf_identifier+'txt', 'r') as fin:
                file_text=fin.readlines()

            # Adding the intercepts values

            for i in range(p,p+8,1):               
                file_text[i] = file_text[i].split('=',1)[0]+'= '
        
            file_text[p] = file_text[p]+str(config['car_intercept'])
            file_text[p+1] = file_text[p+1]+str(config['walk_transit_intercept'])
            file_text[p+2] = file_text[p+2]+str(config['drive_transit_intercept'])
            file_text[p+3] = file_text[p+3]+str(config['ride_hail_transit_intercept'])
            file_text[p+4] = file_text[p+4]+str(config['ride_hail_intercept'])
            file_text[p+5] = file_text[p+5]+str(config['ride_hail_pooled_intercept'])
            file_text[p+6] = file_text[p+6]+str(config['walk_intercept'])
            file_text[p+7] = file_text[p+7]+str(config['bike_intercept'])
                
            for j in range(p,p+8,1):
                file_text[j] = file_text[j]+' \n'

            # Repairing the lastiteration value of the conf file

            for i in range(q,q+1,1):                
                file_text[i] = file_text[i].split('=',1)[0]+'= '
        
            file_text[q] = file_text[q]+finaliteration
                    
            for j in range(q,q+1,1):
                file_text[j] = file_text[j]+' \n'
                
            with open(Repo+'test/input/'+selected_sim+'/'+conf_identifier+'txt', 'w') as fini:
                for i in file_text:
                    fini.write(i)
                   
        def run_beam():
            os.chdir(Repo)            
            subprocess.call([Repo+'runme.sh']) # external file usage runme.sh from beam home
            os.chdir(Current)

        ext_change('edit')
        change_conf(config)            
        ext_change('save')
        run_beam()

        def all_subdirs_of(b='/home/berkeleylab/Repository/beam/output/'+selected_sim+'/'):
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

        # Intermediate iteration stopping
        df1 = pd.read_csv(latest_subdir+"/referenceRealizedModeChoice.csv").iloc[[0, 3]].drop(['iterations'], axis=1)
        extrapolated_coeff = {'bike':0,'car':-2,'cav':2,'drive_transit':0,'ride_hail':-4.5, 'ride_hail_pooled':0,'ride_hail_transit':0, 'walk':4, 'walk_transit':1.5}
        df1 = df1.append(extrapolated_coeff, ignore_index=True)
        df1.loc['3'] = df1.iloc[1:3].sum()
        diff = (df1.iloc[0] - df1.iloc[-1]).abs().sum()
        remains1 = float(diff)

        # Get config ID value
        log_inf = hpres.logged_results_to_HBS_result('/home/berkeleylab/Calib_documentation/TUNE_integrate/TUNE_test/worker_n_optimizer/')
        all_runs = log_inf.get_all_runs()
        jobid_val = all_runs[-1]['config_id']

        def stop_iteration():
            def change_conf_last_iter():
                with open(Repo+'test/input/'+selected_sim+'/'+conf_identifier+'txt', 'r') as fin:
                    file_text=fin.readlines()
                
                for i in range(q,q+1,1):                
                    file_text[i] = file_text[i].split('=',1)[0]+'= '
    
                file_text[q] = file_text[q]+'4'
                
                for j in range(q,q+1,1):
                    file_text[j] = file_text[j]+' \n'
                    
                with open(Repo+'test/input/'+selected_sim+'/'+conf_identifier+'txt', 'w') as fini:
                    for i in file_text:
                        fini.write(i)
                        
            ext_change('edit')
            change_conf_last_iter()
            ext_change('save')

        if diff < threshold:   
            print('Error is below threshold (',threshold,') with ',str(diff),' at jobid ', str(jobid_val))
            
        else:
            stop_iteration()           
            print('Error is above threshold (',threshold,') and difference is ',str(diff),' for jobid ',str(jobid_val))
       
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
    
