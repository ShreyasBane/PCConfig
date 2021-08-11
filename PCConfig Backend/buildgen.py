import pandas as pd
import random

import ml
import db
import compatibility
from vars import cpus, cpus_processed, motherboards, motherboards_processed, rams, rams_processed, gpus, gpus_processed, psus, psus_processed, storages, storages_processed, builds, users, csv_path

def create(category):
  shortlisted_cpus = db.where([['Class', db.eq, category]], cpus)
  shortlisted_cpus = shortlisted_cpus['ID'].tolist()
  
  name_pool = ['Miku', 'Kradness', 'Aimer', 'Womble', 'DECO*27', 'Mafu', 'DAOKO', 'Eureka', 'Yoasobi', 'Nier', 'Nyarons', 'TeaTime', 'Yui', 'UpliftSpice', 'Frou', 'Yoh']

  build1 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': '',
      'motherboard': '',
      'ram': '',
      'gpu': '',
      'storage': '',
      'psu': ''
      }

  build3 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': '',
      'motherboard': '',
      'ram': '',
      'gpu': '',
      'storage': '',
      'psu': ''
      }

  build4 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': '',
      'motherboard': '',
      'ram': '',
      'gpu': '',
      'storage': '',
      'psu': ''
      }

  pos = 0
  cpu = builds['cpu'].value_counts().index[pos]
  while cpu not in shortlisted_cpus:
      pos += 1
      cpu = builds['cpu'].value_counts().index[pos]
  
  build1['cpu'] = cpu

  build1['motherboard'] = ml.mostSelected('motherboard', list(build1.values()), builds.copy())
  build1['ram'] = ml.mostSelected('ram', list(build1.values()), builds.copy())
  build1['gpu'] = ml.mostSelected('gpu', list(build1.values()), builds.copy())
  build1['storage'] = ml.mostSelected('storage', list(build1.values()), builds.copy())
  build1['psu'] = ml.mostSelected('psu', list(build1.values()), builds.copy())

  cpu_features = ['Core Count', 'No of Threads', 'Core Clock', 'Boost Clock', 'TDP', 'Microarchitecture']
  motherboard_features = ['Chipset', 'Form Factor', 'Memory Max', 'Memory Slots', 'PCI-E x16 Slots', 'SATA 6 Gb/s', 'Wireless Networking']
  ram_features = ['Speed', 'Kit Capacity', 'Individual Capacity', 'Modules']
  gpu_features = ['CUDA Cores', 'TDP (W)', 'Memory Size (GB)', 'Effective Memory Clock (Mhz)']
  storage_features = ['Type', 'Capacity', 'Interface']
  psu_features = ['Max Power', 'Energy Rating']
  
  item = db.toList(db.where([['cpuID', db.eq, build1['cpu']]], cpus_processed))[0]
  cpus_data = db.where([['Socket', db.eq, item['Socket']]], cpus_processed)

  index = 'cpuID'
  df = cpus_data
  recommended_cpus = ml.kNNRecommend(build1['cpu'], cpu_features, index, df)

  item = db.toList(db.where([['motherboardID', db.eq, build1['motherboard']]], motherboards_processed))[0]
  motherboards_data = db.where([['Socket', db.eq, item['Socket']]], motherboards_processed)

  index = 'motherboardID'
  df = motherboards_data
  recommended_motherboards = ml.kNNRecommend(build1['motherboard'], motherboard_features, index, df)

  index = 'ramID'
  df = rams_processed
  recommended_rams = ml.kNNRecommend(build1['ram'], ram_features, index, df)

  index = 'gpuID'
  df = gpus_processed
  recommended_gpus = ml.kNNRecommend(build1['gpu'], gpu_features, index, df)

  index = 'storageID'
  df = storages_processed
  recommended_storages = ml.kNNRecommend(build1['storage'], storage_features, index, df)

  index = 'psuID'
  df = psus_processed
  recommended_psus = ml.kNNRecommend(build1['psu'], psu_features, index, df)

  count = 0

  build2 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': recommended_cpus[count],
      'motherboard': recommended_motherboards[count],
      'ram': recommended_rams[count],
      'gpu': recommended_gpus[count],
      'storage': recommended_storages[count],
      'psu': recommended_psus[count]
      }
  while not compatibility.isCompatible(build2):
    build2 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': recommended_cpus[count],
      'motherboard': recommended_motherboards[count],
      'ram': recommended_rams[count],
      'gpu': recommended_gpus[count],
      'storage': recommended_storages[count],
      'psu': recommended_psus[count]
      }
    count += 1

  build3 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': recommended_cpus[count],
      'motherboard': recommended_motherboards[count],
      'ram': recommended_rams[count],
      'gpu': recommended_gpus[count],
      'storage': recommended_storages[count],
      'psu': recommended_psus[count]
      }
  while not compatibility.isCompatible(build3):
    build3 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': recommended_cpus[count],
      'motherboard': recommended_motherboards[count],
      'ram': recommended_rams[count],
      'gpu': recommended_gpus[count],
      'storage': recommended_storages[count],
      'psu': recommended_psus[count]
      }
    count += 1

  build4 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': recommended_cpus[count],
      'motherboard': recommended_motherboards[count],
      'ram': recommended_rams[count],
      'gpu': recommended_gpus[count],
      'storage': recommended_storages[count],
      'psu': recommended_psus[count]
      }
  while not compatibility.isCompatible(build4):
    build4 = {
      'ID': '',
      'name': random.choice(name_pool),
      'userID': '',
      'cpu': recommended_cpus[count],
      'motherboard': recommended_motherboards[count],
      'ram': recommended_rams[count],
      'gpu': recommended_gpus[count],
      'storage': recommended_storages[count],
      'psu': recommended_psus[count]
      }
    count += 1

  datas = [build1, build2, build3, build4]
  # result = []

  for data in datas:
    # final = {}
    if len(data) != 0:
      if data['cpu'] != '':
        temp = db.toList(db.where([['ID', db.eq, data['cpu']]], cpus))
        data['cpu'] = {'ID' : data['cpu'], 'name' : temp[0]['Name']}
      if data['motherboard'] != '':
        temp = db.toList(db.where([['ID', db.eq, data['motherboard']]], motherboards))
        data['motherboard'] = {'ID' : data['motherboard'], 'name' : temp[0]['Name']}
      if data['ram'] != '':
        temp = db.toList(db.where([['ID', db.eq, data['ram']]], rams))
        data['ram'] = {'ID' : data['ram'], 'name' : temp[0]['Name']}
      if data['gpu'] != '':
        temp = db.toList(db.where([['ID', db.eq, data['gpu']]], gpus))
        data['gpu'] = {'ID' : data['gpu'], 'name' : temp[0]['Name']}
      if data['psu'] != '':
        temp = db.toList(db.where([['ID', db.eq, data['psu']]], psus))
        data['psu'] = {'ID' : data['psu'], 'name' : temp[0]['Name']}
      if data['storage'] != '':
        temp = db.toList(db.where([['ID', db.eq, data['storage']]], storages))
        data['storage'] = {'ID' : data['storage'], 'name' : temp[0]['Name']}
    # result.append(final)

  return datas

def findNeed(answers):
  if 'PRO' in answers.values():
      need = 'PRO'
  elif 'MID' in answers.values():
      need = 'MID'
  else:
      need = 'ENTRY'

  return need