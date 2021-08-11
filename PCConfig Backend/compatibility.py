import pandas as pd
import db
from vars import cpus, cpus_processed, motherboards, motherboards_processed, rams, rams_processed, gpus, gpus_processed, psus, psus_processed, storages, storages_processed, builds, users, csv_path

def isCompatible(build):
  cpu, motherboard, ram, gpu, psu, storage = '','','','','',''
  compatibility_mat = {
    'AMD A320': ['Zen', 'Zen+', 'Zen 2'],
    'AMD B350': ['Zen', 'Zen+', 'Zen 2'],
    'AMD X370': ['Zen', 'Zen+', 'Zen 2'],
    'AMD B450': ['Zen', 'Zen+', 'Zen 2', 'Zen 3'],
    'AMD X470': ['Zen', 'Zen+', 'Zen 2', 'Zen 3'],
    'AMD A520': ['Zen 2', 'Zen 3'],
    'AMD B550': ['Zen 2', 'Zen 3'],
    'AMD X570': ['Zen+', 'Zen 2', 'Zen 3'],
    'Intel H410': ['Comet Lake'],
    'Intel B460': ['Comet Lake'],
    'Intel H470': ['Comet Lake'],
    'Intel Q470': ['Comet Lake'],
    'Intel Z490': ['Comet Lake'],
    'Intel H510': ['Comet Lake'],
    'Intel B560': ['Comet Lake'],
    'Intel H570': ['Comet Lake'],
    'Intel Z590': ['Comet Lake'],
    'Intel B250': ['Skylake', 'Kaby Lake'],
    'Intel Q250': ['Skylake', 'Kaby Lake'],
    'Intel H270': ['Skylake', 'Kaby Lake'],
    'Intel Q270': ['Skylake', 'Kaby Lake'],
    'Intel Z270': ['Skylake', 'Kaby Lake'],
    'Intel H310' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'Intel B365' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'Intel B360' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'Intel H370' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'Intel C246' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'Intel Q370' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'Intel Z370' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'Intel Z390' : ['Coffee Lake', 'Coffee Lake Refresh'],
    'AMD X399' : ['Zen', 'Zen+'],
    'AMD TRX40' : ['Zen 2']
  }

  for id in build:
    if id != '':
      if id[0] == 'C':
        cpu = db.toList(db.where([['ID', db.eq, id]], cpus))[0]
      elif id[0] == 'M':
        motherboard = db.toList(db.where([['ID', db.eq, id]], motherboards))[0]
      elif id[0] == 'M':
        ram = db.toList(db.where([['ID', db.eq, id]], rams))[0]
      elif id[0] == 'M':
        gpu = db.toList(db.where([['ID', db.eq, id]], gpus))[0]
      elif id[0] == 'M':
        psu = db.toList(db.where([['ID', db.eq, id]], psus))[0]
      elif id[0] == 'M':
        storage = db.toList(db.where([['ID', db.eq, id]], storages))[0]
      else:
        continue

  result = True
  if cpu != '' and motherboard != '':
    if cpu['Socket'] == motherboard['Socket']:
      if cpu['Microarchitecture'] in compatibility_mat[motherboard['Chipset']]:
        result &= True
      else:
        result &= False
    else:
      result &= False
  if motherboard != '' and ram != '':
    if motherboard['Memory Type'] == ram['Type'] and motherboard['Memory Slots'] >= ram['Modules']:
      result &= True
    else:
      result &= False

  return result