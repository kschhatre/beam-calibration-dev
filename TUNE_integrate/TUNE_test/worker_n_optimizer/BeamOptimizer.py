
import sys
sys.path.insert(1, '/home/berkeleylab/Misc_code/HpBandSter/hpbandster')

import core.nameserver as hpns
import core.result as hpres
from optimizers import BOHB as BOHB
from BeamWorker import BeamWorker

NS = hpns.NameServer(run_id='Beamville', host='127.0.0.1', port=None)
NS.start()


workers=[]
for i in range(3):
   
    w = BeamWorker(nameserver='127.0.0.1', run_id='Beamville', id=i)
    w.run(background=True)
    workers.append(w)
 

result_logger = hpres.json_result_logger(directory='/home/berkeleylab/Calib_documentation/TUNE_integrate/TUNE_test/worker_n_optimizer', overwrite=True)
bohb = BOHB(configspace=w.get_configspace(),run_id='Beamville',min_budget=1, max_budget=3, result_logger=result_logger)
res = bohb.run(n_iterations=3,min_n_workers=3)


bohb.shutdown(shutdown_workers=True)
NS.shutdown()

