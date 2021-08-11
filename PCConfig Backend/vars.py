import pandas as pd
from os.path import join
import numpy as np

######################### DB ###############################
# init db
csv_path = "./csv"
csv_files = ["builds", "cpus", "gfxs", "motherboards", \
 "psus", "rams", "storages", "users"]

cpus = pd.read_csv(join(csv_path, "cpus.csv"))
cpus['index'] = cpus['ID']
cpus = cpus.set_index('index')
cpus = cpus.replace(np.nan, '', regex=True)

cpus_processed = pd.read_csv(join(csv_path, "cpus_processed.csv"))
cpus_processed = cpus_processed.rename(columns={"ID" : "ID2"})
cpus_processed['ID'] = cpus_processed['ID2']
cpus_processed = cpus_processed.set_index('ID')
cpus_processed = cpus_processed.rename(columns={"ID2" : "ID"})
cpus_processed = cpus_processed.rename(columns= {'ID' : 'cpuID'} , inplace=False)
cpus_processed = cpus_processed.replace(np.nan, '', regex=True)

motherboards = pd.read_csv(join(csv_path, "motherboards.csv"))
motherboards['index'] = motherboards['ID']
motherboards = motherboards.set_index('index')
motherboards = motherboards.replace(np.nan, '', regex=True)

motherboards_processed = pd.read_csv(join(csv_path, "motherboards_processed.csv"))
motherboards_processed = motherboards_processed.rename(columns={"ID" : "ID2"})
motherboards_processed['ID'] = motherboards_processed['ID2']
motherboards_processed = motherboards_processed.set_index('ID')
motherboards_processed = motherboards_processed.rename(columns={"ID2" : "ID"})
motherboards_processed =  motherboards_processed.rename(columns={'ID' : 'motherboardID'} , inplace=False)
motherboards_processed = motherboards_processed.replace(np.nan, '', regex=True)

rams = pd.read_csv(join(csv_path, "rams.csv"))
rams['index'] = rams['ID']
rams = rams.set_index('index')
rams = rams.replace(np.nan, '', regex=True)

rams_processed = pd.read_csv(join(csv_path, "rams_processed.csv"))
rams_processed = rams_processed.rename(columns={"ID" : "ID2"})
rams_processed['ID'] = rams_processed['ID2']
rams_processed = rams_processed.set_index('ID')
rams_processed = rams_processed.rename(columns={"ID2" : "ID"})
rams_processed = rams_processed.rename(columns = {'ID': 'ramID'}, inplace = False)
rams_processed = rams_processed.replace(np.nan, '', regex=True)

gpus = pd.read_csv(join(csv_path, "gpus.csv"))
gpus['index'] = gpus['ID']
gpus = gpus.set_index('index')
gpus = gpus.replace(np.nan, '', regex=True)

gpus_processed = pd.read_csv(join(csv_path, "gpus_processed.csv"))
gpus_processed = gpus_processed.rename(columns={"ID" : "ID2"})
gpus_processed['ID'] = gpus_processed['ID2']
gpus_processed = gpus_processed.set_index('ID')
gpus_processed = gpus_processed.rename(columns={"ID2" : "ID"})
gpus_processed = gpus_processed.rename(columns = {'ID': 'gpuID'}, inplace = False)
gpus_processed = gpus_processed.replace(np.nan, '', regex=True)

psus = pd.read_csv(join(csv_path, "psus.csv"))
psus['index'] = psus['ID']
psus = psus.set_index('index')
psus = psus.replace(np.nan, '', regex=True)

psus_processed = pd.read_csv(join(csv_path, "psus_processed.csv"))
psus_processed = psus_processed.rename(columns={"ID" : "ID2"})
psus_processed['ID'] = psus_processed['ID2']
psus_processed = psus_processed.set_index('ID')
psus_processed = psus_processed.rename(columns={"ID2" : "ID"})
psus_processed = psus_processed.rename(columns = {'ID': 'psuID'}, inplace = False)
psus_processed = psus_processed.replace(np.nan, '', regex=True)


storages = pd.read_csv(join(csv_path, "storages.csv"))
storages['index'] = storages['ID']
storages = storages.set_index('index')
storages = storages.replace(np.nan, '', regex=True)

storages_processed = pd.read_csv(join(csv_path, "storages_processed.csv"))
storages_processed = storages_processed.rename(columns={"ID" : "ID2"})
storages_processed['ID'] = storages_processed['ID2']
storages_processed = storages_processed.set_index('ID')
storages_processed = storages_processed.rename(columns={"ID2" : "ID"})
storages_processed = storages_processed.rename(columns = {'ID': 'storageID'}, inplace = False)
storages_processed = storages_processed.replace(np.nan, '', regex=True)

users = pd.read_csv(join(csv_path, "users.csv"))
users['index'] = users['ID']
users = users.set_index('index')
users = users.astype({'password' : 'string'})

builds = pd.read_csv(join(csv_path, "builds.csv"))
builds['index'] = builds['ID']
builds = builds.set_index('index')