import pandas as pd
import functools

# UTILS
def eq(a, b):
  return a == b
def lte(a, b):
  return a <= b
def gte(a, b):
  return a >= b
def lt(a, b):
  return a < b
def gt(a, b):
  return a > b
def inList(a, b):
  return a in b

def add(entry, df):
  table = df.copy()
  try:
    table = table.append(entry, ignore_index=True)
    return table
  except Exception as e:
    print("Error in add", e.__class__, "occurred.")
    return False

# conds = [[key, relation, value], ...]
def delete(conds, table):
  table = table.copy()
  try:
    df1 = table.copy()
    df2 = where(conds, table) 
    df = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    return df.drop(columns = ["_merge"])
  except Exception as e:
    print("Error in delete", e.__class__, "occurred.")
    return False

# conds = [[key, relation, value], ...]
def where(conds, table):
  def check(cond, record):
    [key, relation, value] = cond
    return relation(record[key], value)
  try:
    mapped = list(map(lambda x: check(x, table), conds))
    reduced_cond = functools.reduce(lambda a, b: a | b, mapped[1:], mapped[0])
    return table.loc[reduced_cond]
  except Exception as e:
    print("Error in where", e.__class__, "occurred.")
    return False

# merge dfa and dfb
def merge(dfa, dfb, cols = ["id"]):
  joined = pd.concat([dfa, dfb])
  return joined.drop_duplicates(subset = cols)

def union(dfa, dfb):
  df = dfa.append(dfb, ignore_index=True)
  df = df.drop_duplicates()
  return df

def intersection(dfa, dfb):
  return pd.merge(dfa, dfb, how = "inner", on = list(dfa.columns))

def difference(dfa, dfb):
  merged = dfa.merge(dfb,indicator = True, how='left').loc[lambda x : x['_merge']!='both']
  return merged.drop(columns=["_merge"])

def toList(df):
  df = df.copy()
  return df.to_dict('records')

def edit(df, id, index, value):
  df = df.copy()
  df.at[id, index] = value
  return df

def incrementID(df):
  return df['ID'].tolist()[-1][0] + str(int(df['ID'].tolist()[-1][1:]) + 1)