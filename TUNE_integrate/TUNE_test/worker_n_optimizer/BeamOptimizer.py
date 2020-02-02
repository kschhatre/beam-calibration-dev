
import shutil, os, glob, sys
sys.path.insert(1, '/home/berkeleylab/Misc_code/HpBandSter/hpbandster')
import core.nameserver as hpns
import core.result as hpres
from optimizers import BOHB as BOHB
from BeamWorker import BeamWorker

NS = hpns.NameServer(run_id='BEAM', host='127.0.0.1', port=None)
NS.start()

# User defined variables
Repo='/home/berkeleylab/Repository/beam/test/input/'
no_of_workers = 4
selection = 'beamville' 
#selection is 'beamville' or 'urbansim-1k' or 'urbansim-10k' -> to be update in configselector.py too


if selection == 'beamville':
    Repo = Repo+'beamville/'
    conf = 'beam'
else:
    Repo = Repo+'sf-light/'
    conf = selection
    
def create_conf_copies(no_of_workers):
    for num in range(no_of_workers):
        shutil.copy(Repo+conf+'.conf',Repo+conf+'_'+str(num+1)+'.conf')
        
create_conf_copies(no_of_workers)

workers=[]
for i in range(no_of_workers):   
    w = BeamWorker(nameserver='127.0.0.1', run_id='BEAM', id=i)
    w.run(background=True)
    workers.append(w)

result_logger = hpres.json_result_logger(directory='/home/berkeleylab/Calib_documentation/TUNE_integrate/TUNE_test/worker_n_optimizer', overwrite=True)
bohb = BOHB(configspace=w.get_configspace(),run_id='BEAM',min_budget=1, max_budget=5, result_logger=result_logger)
res = bohb.run(n_iterations=4,min_n_workers=no_of_workers)

id2config = res.get_id2config_mapping()
incumbent = res.get_incumbent_id()
all_runs = res.get_all_runs()

print('best config:', id2config[incumbent]['config'] )
print('total unique configs:', len(id2config.keys()) )
print('total executed runs:', len(all_runs) )
print('total budget corresponds to these function evaluations:', (sum([r.budget for r in all_runs])/243))
print('total elapsed time', (all_runs[-1].time_stamps['finished']-all_runs[0].time_stamps['started']))

bohb.shutdown(shutdown_workers=True)
NS.shutdown()

'''
# Delete conf copies
for filename in glob.glob('/home/berkeleylab/Repository/beam/test/input/beamville/beam_*.conf'): 
    os.remove(filename) 

'''






