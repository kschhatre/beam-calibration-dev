import pandas as pd 
import os


def all_subdirs_of(b='/home/berkeleylab/Repository/beam/output/beamville/'):
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd): result.append(bd)
    return result
        
latest_subdir = max(all_subdirs_of(), key=os.path.getmtime)


df1 = pd.read_csv(latest_subdir+"/referenceRealizedModeChoice.csv").iloc[[0, 3]].drop(['iterations'], axis=1)
extrapolated_coeff = {'bike':0,'car':-2,'cav':2,'drive_transit':0,'ride_hail':-4.5, 'ride_hail_pooled':0,'ride_hail_transit':0, 'walk':4, 'walk_transit':1.5}
df1 = df1.append(extrapolated_coeff, ignore_index=True)
df1.loc['3'] = df1.iloc[1:3].sum()
diff = (df1.iloc[0] - df1.iloc[-1]).abs().sum()
        


exit(diff)