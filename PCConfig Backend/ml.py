import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import NearestNeighbors

def mostSelected(category, build, builds):
  selected_users = builds.copy()
  for char in build:
    if char != '':
      if char[0] == 'C':
        index = 'cpu'
        selected_users_cpu = selected_users.loc[selected_users['cpu'] == char , 'userID']
        if not selected_users_cpu.empty:
          selected_users_cpu_list = selected_users_cpu.tolist()
          selected_users = selected_users[selected_users.userID.isin(selected_users_cpu_list)]

      elif char[0] == 'M':
        index = 'motherboard'
        selected_users_motherboard = selected_users.loc[selected_users['motherboard'] == char , 'userID']
        if not selected_users_motherboard.empty:
          selected_users_motherboard_list = selected_users_motherboard.tolist()
          selected_users = selected_users[selected_users.userID.isin(selected_users_motherboard_list)]
      

      elif char[0] == 'R':
        index = 'ram'
        selected_users_ram = selected_users.loc[selected_users['ram'] == char , 'userID']
        if not selected_users_ram.empty:
          selected_users_ram_list = selected_users_ram.tolist()
          selected_users = selected_users[selected_users.userID.isin(selected_users_ram_list)]

      elif char[0] == 'G':
        index = 'gpu'
        selected_users_gpu = selected_users.loc[selected_users['gpu'] == char , 'userID']
        if not selected_users_gpu.empty:
          selected_users_gpu_list = selected_users_gpu.tolist()
          selected_users = selected_users[selected_users.userID.isin(selected_users_gpu_list)]

      elif char[0] == 'P':
        index = 'psu'
        selected_users_psu = selected_users.loc[selected_users['psu'] == char , 'userID']
        if not selected_users_psu.empty:
          selected_users_psu_list = selected_users_psu.tolist()
          selected_users = selected_users[selected_users.userID.isin(selected_users_psu_list)]

      elif char[0] == 'S':
        index = 'storage'
        selected_users_storage = selected_users.loc[selected_users['storage'] == char , 'userID']
        if not selected_users_storage.empty:
          selected_users_storage_list = selected_users_storage.tolist()
          selected_users = selected_users[selected_users.userID.isin(selected_users_storage_list)]

      else:
        index = 'null'
  
  items = selected_users[category].value_counts().index
  count = 0
  try:
    while items[count] == '':
      count += 1
    return items[count]
  except IndexError:
    items = builds[category].value_counts().index
    while items[count] == '':
      count += 1
    return items[count]

def kNNRecommend(most_selected_item, features, index, dfm):
  df = dfm.copy()
  main_data = df[[index] + features]
  main_data = pd.melt(main_data, id_vars= index , value_vars = main_data.columns[1:] ,var_name='Features', value_name='Value')
  
  main_data_pivot = main_data.pivot_table(index = index, columns = 'Features' , values = 'Value').sort_values(by = [index])
  main_data_pivot[features] = StandardScaler().fit_transform(main_data_pivot[features])
  main_data_matirx = csr_matrix(main_data_pivot.values)

  model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
  model_knn.fit(main_data_matirx)

  indexes = list(main_data_pivot.index)
  query_index = indexes.index(most_selected_item)

  distances, indices = model_knn.kneighbors(main_data_pivot.iloc[query_index,].values.reshape(1, -1), n_neighbors = 7)

  item_prediction_list = []
  for i in range(0, len(distances.flatten())):
    if i == 0:
      continue
    else:
      item_prediction_list.append(main_data_pivot.index[indices.flatten()[i]])

  return item_prediction_list