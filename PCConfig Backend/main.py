import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import functools
import pandas as pd
import numpy as np
from os.path import join

import db
import ml
import buildgen
import compatibility
from vars import cpus, cpus_processed, motherboards, motherboards_processed, rams, rams_processed, gpus, gpus_processed, psus, psus_processed, storages, storages_processed, builds, users, csv_path

# MAIN APP
######################### INIT APP ##########################
app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# /login
# /signup
# /user/id
# /user/userid/build
# /user/userid/build/bid
# /user/userid/build/bid/(add|remove)
# /product/info
# /product/(cpus|gpus|psus|storages|rams|motherboards)
# /product/(cpus|gpus|psus|storages|rams|motherboards)/filter
########################### ROUTES ########################### 
# ROOT
@app.get("/")
async def root():
  return {"test": "test"}

# LOGIN
# @app.options("**/*")
# async def loginPrehandler(request: Request, response: Response):
#   response.status_code = status.HTTP_200_OK 

# input : {
#  username,
#  password
# }
@app.post("/login")
async def loginHandler(request: Request):
  payload = await request.json()
  present = []
  present = db.toList(db.intersection(\
      db.where([['username', db.eq, payload['username']]],users),\
      db.where([['password', db.eq, payload['password']]],users)\
  ))
  if (len(present) == 0):
    return {"status": False, "message": "No user exists"}
  else:
    # todo
    # also return userID key in below dict
    return {"status": True, "message" : "Login successfull", \
     "userID": present[0]["ID"], "username": present[0]['username']}


# SIGNUP
@app.options("/signup")
async def signupPrehandler(request: Request, response: Response):
  response.status_code = status.HTTP_200_OK 

# input {
#  username,
#  email,
#  password,
# }
@app.post("/signup")
async def signupHandler(request: Request):
  global users
  payload = await request.json()
  present = db.toList(db.union(\
      db.where([['username', db.eq, payload['username']]], users), \
      db.where([['email', db.eq, payload['email']]], users) \
    ))
  # not present, make accountusers
  if (len(present) == 0):
    payload['ID'] = db.incrementID(users)
    users = db.add(payload, users)
    users.to_csv(join(csv_path, "users_backup.csv"), index=False)
    return {"status": True, "message" : "Signup successfull"}
  # usersentusers
  else:
    return {"status": False, "message" : "Account already exists"}

# FILTER CONTENTS
# CPU
# type
# input
# output : [
#   {name: Attribute,
#    options : Possible Values },
# ]
@app.get("/product/cpus/filter")
async def cpuFilter():
  cpufilterkeys = [
    {"name": "Manufacturer" , "options": cpus['Manufacturer'].unique().tolist()},
    {"name": "Microarchitecture" ,"options": cpus['Microarchitecture'].unique().tolist()},
    {"name": "Core Count", "options" : cpus['Core Count'].unique().tolist()},
    {"name": "No of Threads" ,"options": cpus['No of Threads'].unique().tolist()},
    {"name": "Socket" ,"options": cpus['Socket'].unique().tolist()}
  ]
  return cpufilterkeys

# MOTHERBOARD
@app.get("/product/motherboards/filter")
def motherboardFilter():
  motherboardfilterkeys = [
    {"name": "Manufacturer", 'options': motherboards['Manufacturer'].unique().tolist()},
    {"name": "Socket", 'options': motherboards['Socket'].unique().tolist()},
    {"name": "Form Factor", 'options': motherboards['Form Factor'].unique().tolist()},
    {"name": "Chipset", 'options': motherboards['Chipset'].unique().tolist()},
    {"name": "Memory Slots", 'options': motherboards['Memory Slots'].unique().tolist()},
    {"name": "Memory Max", 'options': motherboards['Memory Max'].unique().tolist()}
  ]
  return motherboardfilterkeys

# RAM
@app.get("/product/rams/filter")
def ramFilter():
 ramfilterkeys = [
    {"name": "Manufacturer", 'options': rams['Manufacturer'].unique().tolist()},
    {"name": "Speed", 'options': rams['Speed'].unique().tolist()},
    {"name": "Kit Capacity", 'options': rams['Kit Capacity'].unique().tolist()},
    {"name": "Modules", 'options': rams['Modules'].unique().tolist()}
 ]
 return ramfilterkeys

# GPU
@app.get("/product/gpus/filter")
def gpuFilter():
  gpufilterkeys = [
    {"name": "Manufacturer", 'options': gpus['Manufacturer'].unique().tolist()},
    {"name": "Chipset Manufacturer", 'options': gpus['Chipset Manufacturer'].unique().tolist()},
    {"name": "GPU", 'options': gpus['GPU'].unique().tolist()},
    {"name": "Memory Size (GB)", 'options': gpus['Memory Size (GB)'].unique().tolist()},
    {"name": "Memory Type", 'options': gpus['Memory Type'].unique().tolist()}
  ]
  return gpufilterkeys

# PSU
@app.get("/product/psus/filter")
def psuFilter():
  psufilterkeys = [
    {"name": "Manufacturer", 'options': psus['Manufacturer'].unique().tolist()},
    {"name": "Type", 'options': psus['Type'].unique().tolist()},
    {"name": "Max Power", 'options': psus['Max Power'].unique().tolist()},
    {"name": "Modular", 'options': psus['Modular'].unique().tolist()},
    {"name": "Energy Rating", 'options': psus['Energy Rating'].unique().tolist()}
  ]
  return psufilterkeys

# Storage
@app.get("/product/storages/filter")
def storageFilter():
  storagefilterkeys = [
    {"name": "Manufacturer", 'options': storages['Manufacturer'].unique().tolist()},
    {"name": "Type", 'options': storages['Type'].unique().tolist()},
    {"name": "Interface", 'options': storages['Interface'].unique().tolist()},
    {"name": "Capacity", 'options': storages['Capacity'].unique().tolist()},
    {"name": "Form Factor", 'options': storages['Form Factor'].unique().tolist()}
  ]
  return storagefilterkeys

## FILTER UTILS
# CPU Search

# input {
#   key: val, ...
# }
@app.post("/product/cpus/")
async def searchCpu(request: Request):
  payload = await request.json()
  
  def check(x, payload, index):
    try:
      if payload[index]:
        return x[index] in payload[index] or len(payload[index]) == 0
      else:
        return True
    except KeyError:
        return True

  filtered = list(filter(lambda x: \
  check(x, payload, 'Manufacturer') and \
  check(x, payload, 'Microarchitecture') and \
  check(x, payload, 'Core Count') and \
  check(x, payload, 'No of Threads') and \
  check(x, payload, 'Socket'), db.toList(cpus)))
     
  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Core Count" : entry["Core Count"], \
        "No of Threads" : entry["No of Threads"], \
        "Core Clock" : entry["Core Clock"], \
        "Boost Clock" : entry["Boost Clock"] \
      } \
  }, filtered))
  return result

# Motherboard Search

# input {
#   key: val, ...
# }
@app.post("/product/motherboards/")
async def searchMotherboard(request: Request):
  payload = await request.json()
  
  def check(x, payload, index):
    try:
      if payload[index]:
        return x[index] in payload[index] or len(payload[index]) == 0
      else:
        return True
    except KeyError:
        return True

  filtered = list(filter(lambda x: \
  check(x, payload, 'Manufacturer') and \
  check(x, payload, 'Socket') and \
  check(x, payload, 'Form Factor') and \
  check(x, payload, 'Memory Max') and \
  check(x, payload, 'Chipset') and \
  check(x, payload, 'Memory Slots'), db.toList(motherboards)))
     
  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Socket" : entry["Socket"], \
        "Chipset" : entry["Chipset"], \
        "Form Factor" : entry["Form Factor"], \
        "Memory Slots" : entry["Memory Slots"] \
      } \
  }, filtered))
  return result

# RAM Search

# input {
#   key: val, ...
# }
@app.post("/product/rams/")
async def searchRam(request: Request):
  payload = await request.json()
  
  def check(x, payload, index):
    try:
      if payload[index]:
        return x[index] in payload[index] or len(payload[index]) == 0
      else:
        return True
    except KeyError:
        return True

  filtered = list(filter(lambda x: \
  check(x, payload, 'Manufacturer') and \
  check(x, payload, 'Speed') and \
  check(x, payload, 'Kit Capacity') and \
  check(x, payload, 'Modules'), db.toList(rams)))
     
  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Speed" : entry["Speed"], \
        "Timings" : entry["Timings"], \
        "Kit Capacity" : entry["Kit Capacity"], \
        "Modules" : entry["Modules"] \
      } \
  }, filtered))
  return result

# GPU Search

# input {
#   key: val, ...
# }
@app.post("/product/gpus/")
async def searchGpu(request: Request):
  payload = await request.json()
  
  def check(x, payload, index):
    try:
      if payload[index]:
        return x[index] in payload[index] or len(payload[index]) == 0
      else:
        return True
    except KeyError:
        return True

  filtered = list(filter(lambda x: \
  check(x, payload, 'Manufacturer') and \
  check(x, payload, 'Chipset Manufacturer') and \
  check(x, payload, 'GPU') and \
  check(x, payload, 'Memory Size (GB)') and \
  check(x, payload, 'Memory Type'), db.toList(gpus)))
     
  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Core Clock (Mhz)" : entry["Core Clock (Mhz)"], \
        "Boost Clock (Mhz)" : entry["Boost Clock (Mhz)"], \
        "Memory Size (GB)" : entry["Memory Size (GB)"], \
        "Memory Type" : entry["Memory Type"] \
      } \
  }, filtered))
  return result

# Psu Search

# input {
#   key: val, ...
# }
@app.post("/product/psus/")
async def searchPsu(request: Request):
  payload = await request.json()
  
  def check(x, payload, index):
    try:
      if payload[index]:
        return x[index] in payload[index] or len(payload[index]) == 0
      else:
        return True
    except KeyError:
        return True

  filtered = list(filter(lambda x: \
  check(x, payload, 'Manufacturer') and \
  check(x, payload, 'Type') and \
  check(x, payload, 'Modular') and \
  check(x, payload, 'Max Power') and \
  check(x, payload, 'Energy Rating'), db.toList(psus)))
     
  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Max Power" : entry["Max Power"], \
        "Modular" : entry["Modular"], \
        "Energy Rating" : entry["Energy Rating"], \
        "Type" : entry["Type"] \
      } \
  }, filtered))
  return result

# Storage Search

# input {
#   key: val, ...
# }
@app.post("/product/storages/")
async def searchStorage(request: Request):
  payload = await request.json()
  
  def check(x, payload, index):
    try:
      if payload[index]:
        return x[index] in payload[index] or len(payload[index]) == 0
      else:
        return True
    except KeyError:
        return True


  filtered = list(filter(lambda x: \
  check(x, payload, 'Manufacturer') and \
  check(x, payload, 'Type') and \
  check(x, payload, 'Interface') and \
  check(x, payload, 'Capacity') and \
  check(x, payload, 'Form Factor'), db.toList(storages)))
     
  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Type" : entry["Type"], \
        "Capacity" : entry["Capacity"], \
        "Interface" : entry["Interface"], \
        "Form Factor" : entry["Form Factor"] \
      } \
  }, filtered))
  return result

#Product info
#/product/info/id
@app.get("/product/info/{id}")
async def productInfo(id: str = 'C1'):
  if id[0] == 'C':
    data = db.toList(db.where([['ID', db.eq, id]], cpus))
  elif id[0] == 'M':
    data = db.toList(db.where([['ID', db.eq, id]], motherboards))
  elif id[0] == 'R':
    data = db.toList(db.where([['ID', db.eq, id]], rams))
  elif id[0] == 'G':
    data = db.toList(db.where([['ID', db.eq, id]], gpus))
  elif id[0] == 'P':
    data = db.toList(db.where([['ID', db.eq, id]], psus))
  elif id[0] == 'S':
    data = db.toList(db.where([['ID', db.eq, id]], storages))
  else:
    data = [{}]
  data = data[0]
  details = {}
  for key in data.keys():
    if key not in ['ID', "Name"]:
      details[key] = data[key]

  result = {
    'ID': data['ID'],
    'image': "https://picsum.photos/150",
    'productName': data['Name'],
    'details': details
  }
  return result


#Build UTILS
#Get Builds
#Get build component names
@app.get("/user/build/{buildID}/names")
async def getItemNames(buildID: str = 'B1'):
  data = db.toList(db.where([['ID', db.eq, buildID]], builds))
  result ={}
  if len(data) != 0:
    if data[0]['cpu'] != '':
      temp = db.toList(db.where([['ID', db.eq, data[0]['cpu']]], cpus))
      result['cpu'] = temp[0]['Name']
    if data[0]['motherboard'] != '':
      temp = db.toList(db.where([['ID', db.eq, data[0]['motherboard']]], motherboards))
      result['motherboard'] = temp[0]['Name']
    if data[0]['ram'] != '':
      temp = db.toList(db.where([['ID', db.eq, data[0]['ram']]], rams))
      result['ram'] = temp[0]['Name']
    if data[0]['gpu'] != '':
      temp = db.toList(db.where([['ID', db.eq, data[0]['gpu']]], gpus))
      result['gpu'] = temp[0]['Name']
    if data[0]['psu'] != '':
      temp = db.toList(db.where([['ID', db.eq, data[0]['psu']]], psus))
      result['psu'] = temp[0]['Name']
    if data[0]['storage'] != '':
      temp = db.toList(db.where([['ID', db.eq, data[0]['storage']]], storages))
      result['storage'] = temp[0]['Name']

    return result
  else:
    return {}

@app.get("/user/{userID}/builds")
async def getBuilds(userID: str = 'U1'):
  data = db.toList(db.where([['userID', db.eq, userID]], builds))
  return data

#Create Build
@app.get("/user/{userID}/builds/new/{name}")
async def createBuild(userID: str = 'U1', name: str = 'foo'):
  global builds
  data = {'ID': db.incrementID(builds),
          'name' : name,
          'userID': userID,
          'cpu': '',
          'motherboard': '',
          'ram': '',
          'gpu': '',
          'storage': '',
          'psu': ''}
  builds.loc[db.incrementID(builds)] = [db.incrementID(builds), name, userID, '', '', '', '', '', '']
  builds.to_csv(join(csv_path, "builds_backup.csv"), index=False)
  return data

#Get Build Info
@app.get("/user/build/{buildID}")
async def buildInfo(buildID: str = 'B1'):
  data = db.toList(db.where([['ID', db.eq, buildID]], builds))
  if len(data) != 0:
    status = compatibility.isCompatible(data[0])
    return {'build' : data[0], 'status' : status}
  else:
    return {}

#Add Item to build
@app.get("/user/build/{id}/modify/{item}")
async def buildAdd(id: str = 'C1', item: str = ''):
  global builds
  if item[0] == 'C':
    builds = db.edit(builds, id, 'cpu', item)
  elif item[0] == 'M':
    builds = db.edit(builds, id, 'motherboard', item)
  elif item[0] == 'R':
    builds = db.edit(builds, id, 'ram', item)
  elif item[0] == 'G':
    builds = db.edit(builds, id, 'gpu', item)
  elif item[0] == 'P':
    builds = db.edit(builds, id, 'psu', item)
  elif item[0] == 'S':
    builds = db.edit(builds, id, 'storage', item)
  else:
    data = [{}]
  builds.to_csv(join(csv_path, "builds_backup.csv"), index=False)
  return {'status': 'success'}

#Delete build
@app.get("/user/build/{id}/delete")
async def deleteBuild(id: str = ''):
  global builds
  builds = builds.drop(index=id)
  builds.to_csv(join(csv_path, "builds_backup.csv"), index=False)
  return {'status': 'success'}


#Recommend CPU
@app.get("/recommend/{buildID}/cpus")
async def recommendCpu(buildID: str):
  global builds
  global cpus_processed
  global cpus
  category = 'cpu'
  build = db.toList(db.where([['ID', db.eq, buildID]], builds))[0]
  build = list(build.values())
  most_selected_item = ml.mostSelected(category, build, builds.copy())

  item = db.toList(db.where([['cpuID', db.eq, most_selected_item]], cpus_processed))[0]
  cpus_data = db.where([['Socket', db.eq, item['Socket']]], cpus_processed)

  features = ['Core Count', 'No of Threads', 'Core Clock', 'Boost Clock', 'TDP', 'Microarchitecture']
  index = 'cpuID'
  df = cpus_data
  recommended_items = ml.kNNRecommend(most_selected_item, features, index, df)

  recommends = []

  for item in recommended_items:
    recommends.append(db.toList(db.where([['ID', db.eq, item]], cpus))[0])

  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Core Count" : entry["Core Count"], \
        "No of Threads" : entry["No of Threads"], \
        "Core Clock" : entry["Core Clock"], \
        "Boost Clock" : entry["Boost Clock"] \
      } \
  }, recommends))

  return result

#Recommend Motherboard
@app.get("/recommend/{buildID}/motherboards")
async def recommendMotherboard(buildID: str):
  global builds
  global motherboards_processed
  global motherboards
  category = 'motherboard'
  build = db.toList(db.where([['ID', db.eq, buildID]], builds))[0]
  build = list(build.values())
  most_selected_item = ml.mostSelected(category, build, builds.copy())

  item = db.toList(db.where([['motherboardID', db.eq, most_selected_item]], motherboards_processed))[0]
  motherboards_data = db.where([['Socket', db.eq, item['Socket']]], motherboards_processed)

  features = ['Chipset', 'Form Factor', 'Memory Max', 'Memory Slots', 'PCI-E x16 Slots', 'SATA 6 Gb/s', 'Wireless Networking']
  index = 'motherboardID'
  df = motherboards_data
  recommended_items = ml.kNNRecommend(most_selected_item, features, index, df)

  recommends = []

  for item in recommended_items:
    recommends.append(db.toList(db.where([['ID', db.eq, item]], motherboards))[0])

  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Socket" : entry["Socket"], \
        "Chipset" : entry["Chipset"], \
        "Form Factor" : entry["Form Factor"], \
        "Memory Slots" : entry["Memory Slots"] \
      } \
  }, recommends))
  return result

#Recommend Rams
@app.get("/recommend/{buildID}/rams")
async def recommendRam(buildID: str):
  global builds
  global rams_processed
  global rams
  category = 'ram'
  build = db.toList(db.where([['ID', db.eq, buildID]], builds))[0]
  build = list(build.values())
  most_selected_item = ml.mostSelected(category, build, builds.copy())

  features = ['Speed', 'Kit Capacity', 'Individual Capacity', 'Modules']
  index = 'ramID'
  df = rams_processed
  recommended_items = ml.kNNRecommend(most_selected_item, features, index, df)

  recommends = []

  for item in recommended_items:
    recommends.append(db.toList(db.where([['ID', db.eq, item]], rams))[0])

  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Speed" : entry["Speed"], \
        "Timings" : entry["Timings"], \
        "Kit Capacity" : entry["Kit Capacity"], \
        "Modules" : entry["Modules"] \
      } \
  }, recommends))
  return result

#Recommend gpus
@app.get("/recommend/{buildID}/gpus")
async def recommendGpu(buildID: str):
  global builds
  global gpus_processed
  global gpus
  category = 'gpu'
  build = db.toList(db.where([['ID', db.eq, buildID]], builds))[0]
  build = list(build.values())
  most_selected_item = ml.mostSelected(category, build, builds.copy())

  features = ['CUDA Cores', 'TDP (W)', 'Memory Size (GB)', 'Effective Memory Clock (Mhz)']
  index = 'gpuID'
  df = gpus_processed
  recommended_items = ml.kNNRecommend(most_selected_item, features, index, df)

  recommends = []

  for item in recommended_items:
    recommends.append(db.toList(db.where([['ID', db.eq, item]], gpus))[0])

  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Core Clock (Mhz)" : entry["Core Clock (Mhz)"], \
        "Boost Clock (Mhz)" : entry["Boost Clock (Mhz)"], \
        "Memory Size (GB)" : entry["Memory Size (GB)"], \
        "Memory Type" : entry["Memory Type"] \
      } \
  }, recommends))
  return result

#Recommend storages
@app.get("/recommend/{buildID}/storages")
async def recommendStorage(buildID: str):
  global builds
  global storages_processed
  global storages
  category = 'storage'
  build = db.toList(db.where([['ID', db.eq, buildID]], builds))[0]
  build = list(build.values())
  most_selected_item = ml.mostSelected(category, build, builds.copy())

  features = ['Type', 'Capacity', 'Interface']
  index = 'storageID'
  df = storages_processed
  recommended_items = ml.kNNRecommend(most_selected_item, features, index, df)

  recommends = []

  for item in recommended_items:
    recommends.append(db.toList(db.where([['ID', db.eq, item]], storages))[0])

  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Type" : entry["Type"], \
        "Capacity" : entry["Capacity"], \
        "Interface" : entry["Interface"], \
        "Form Factor" : entry["Form Factor"] \
      } \
  }, recommends))
  return result

#Recommend psus
@app.get("/recommend/{buildID}/psus")
async def recommendPsus(buildID: str):
  global builds
  global psus_processed
  global psus
  category = 'psu'
  build = db.toList(db.where([['ID', db.eq, buildID]], builds))[0]
  build = list(build.values())
  most_selected_item = ml.mostSelected(category, build, builds.copy())

  features = ['Max Power', 'Energy Rating']
  index = 'psuID'
  df = psus_processed
  recommended_items = ml.kNNRecommend(most_selected_item, features, index, df)

  recommends = []

  for item in recommended_items:
    recommends.append(db.toList(db.where([['ID', db.eq, item]], psus))[0])

  result = list(map(lambda entry: {\
      "ID" : entry['ID'], \
      "name" : entry['Name'], \
      "imageUrl": "https://picsum.photos/100", \
      "details" : { \
        "Max Power" : entry["Max Power"], \
        "Modular" : entry["Modular"], \
        "Energy Rating" : entry["Energy Rating"], \
        "Type" : entry["Type"] \
      } \
  }, recommends))
  return result

#Generate build
@app.options("/generate")
async def generatePrehandler(request: Request, response: Response):
  response.status_code = status.HTTP_200_OK 

@app.post("/generate")
async def generateHandler(request: Request):
  payload = await request.json()
  need = buildgen.findNeed(payload)
  build = buildgen.create(need)
  return build

# SERVER START
if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8080,reload=True, workers=2)