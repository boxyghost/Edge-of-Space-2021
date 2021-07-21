# -*- coding: utf-8 -*-
"""New NGC EOS Databoard Data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10UNXxnIms225faBUcaPyGye9eKGZRj3c

**Importing libraries that we will use**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display # Allows the use of display() for DataFrames

"""**Uploading the CSV**"""

dataset = pd.read_csv('CoolTerm Capture 2020-07-28 08-17-55.csv',header=None)

dataset

"""**Deleting features we will not use**"""

del dataset[15] 
del dataset[16]
del dataset[4]
del dataset[5]
del dataset[6]

dataset

"""**Renaming the column entries to their rightful names**"""

dataset.rename(columns={1: "TVOC", 3: "eCO2", 8: "Temperature", 10: "Pressure", 12: "Altitude", 14: "Humidity", 18: "X_Ori", 20: "Y_Ori", 22: "Z_Ori"})

"""**Deleting the columns that saved us column names in the original CSV**"""

del dataset[0] 
del dataset[2]
del dataset[7]
del dataset[9]
del dataset[11]
del dataset[13]
del dataset[17]
del dataset[19]
del dataset[21]

dataset

"""**HAD TO RENAME AGAIN BECAUSE IT BUGGED IDK WHY BUT IT WORKS**"""

dataset.rename(columns={1: "TVOC", 3: "eCO2", 8: "Temperature", 10: "Pressure", 12: "Altitude", 14: "Humidity", 18: "X_Ori", 20: "Y_Ori", 22: "Z_Ori"},inplace=True)

"""**Saving the dataframe to a new CSV**"""

dataset.to_csv(r'newCoolTempData.csv')

"""---



---

**Redo all over again for a new csv**
"""

dataset2 = pd.read_csv('datalogger_ACM0_2020-07-28-15_53_54.csv',header=None)