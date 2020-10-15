import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from nuueomueller import Luchiman, Mueller


database = pd.read_csv('Lu_chipman.csv',index_col='wavelength')

wavelength = pd.Series.tolist(database.index)
element =  pd.Series.tolist(database.columns)

#將Database數據轉為變數陣列
for i in range(1,5):
    for j in range(1,5):
        element_str = str(f'M{i}{j}')
        exec(f'M{i}{j}'+ '=' + f'pd.Series.tolist(database.M{i}{j})')  

num = len(wavelength) #總運算次數
D_value = []
P_value = []
Delta_value =[]
R_value =[]
linear_value = []
opticalactivity_value = []
theta_value = []
diattenuationMatrix = []
depolarizationMatrix = []
retardanceMatrix = []
for m in range(4):
    for n in range(4):
        exec(f'diattenuationM{m}{n}=[]')
        exec(f'retardanceM{m}{n} =[]')
        exec(f'depolarizationM{m}{n}=[]')

for i in range(num):
    muellermatrix = np.array([[M11[i],M12[i],M13[i],M14[i]],
                             [M21[i],M22[i],M23[i],M24[i]],
                             [M31[i],M32[i],M33[i],M34[i]],
                             [M41[i],M42[i],M43[i],M44[i]]])

    lc = Luchiman(muellermatrix)
    D_value += [lc.diattenuation('D_value')]
    P_value += [lc.diattenuation('P_value')]
    Delta_value += [lc.depolarization('Delta_value')]
    diattenuationMatrix += [lc.diattenuation('matrix')]
    depolarizationMatrix += [lc.depolarization('matrix')]
    retardanceMatrix += [lc.retardance('matrix')]
    # 極分解矩陣
    for m in range(4):
        for n in range(4):
            exec(f'diattenuationM{m}{n} += [lc.diattenuation("matrix")[{m},{n}]]')
            exec(f'retardanceM{m}{n}+= [lc.retardance("matrix")[{m},{n}]]')
            exec(f'depolarizationM{m}{n} += [lc.depolarization("matrix")[{m},{n}]]')

    R_value += [lc.retardancevalue('R_value')]
    linear_value += [lc.retardancevalue('linear')]
    opticalactivity_value += [lc.retardancevalue('opticalactivity')]
    theta_value += [lc.retardancevalue('theta')]

#運算結果儲存至Excel
all_list = [D_value,P_value,Delta_value,R_value,linear_value,opticalactivity_value,theta_value]
datat = pd.DataFrame(all_list)
data = datat.T
data.index = wavelength
data.columns = ['D','P','Delta','R','linear','opticalactivity','theta']

diattenuation  = [diattenuationM00,diattenuationM01,diattenuationM02,diattenuationM03,
                  diattenuationM10,diattenuationM11,diattenuationM12,diattenuationM13,
                  diattenuationM20,diattenuationM21,diattenuationM22,diattenuationM23,
                  diattenuationM30,diattenuationM31,diattenuationM32,diattenuationM33,]
diattenuation = pd.DataFrame(diattenuation)
diattenuation = diattenuation.T
diattenuation.index= wavelength
diattenuation.columns=element

retardance  = [retardanceM00,retardanceM01,retardanceM02,retardanceM03,
                  retardanceM10,retardanceM11,retardanceM12,retardanceM13,
                  retardanceM20,retardanceM21,retardanceM22,retardanceM23,
                  retardanceM30,retardanceM31,retardanceM32,retardanceM33,]
retardance = pd.DataFrame(retardance)
retardance = retardance.T
retardance.index= wavelength
retardance.columns=element

depolarization  = [depolarizationM00,depolarizationM01,depolarizationM02,depolarizationM03,
                  depolarizationM10,depolarizationM11,depolarizationM12,depolarizationM13,
                  depolarizationM20,depolarizationM21,depolarizationM22,depolarizationM23,
                  depolarizationM30,depolarizationM31,depolarizationM32,depolarizationM33,]
depolarization = pd.DataFrame(depolarization)
depolarization = depolarization.T
depolarization.index= wavelength
depolarization.columns=element
'''
#儲存Excel
with pd.ExcelWriter('output.xlsx') as writer:
    data.to_excel(writer,sheet_name='DATA')
    diattenuation.to_excel(writer,sheet_name='diattenuation')
    retardance.to_excel(writer,sheet_name='retardance')
    depolarization.to_excel(writer,sheet_name='depolarization')
'''

#儲存Csv
os.mkdir('output')
data.to_csv('output\\DATA.csv')
diattenuation.to_csv('output\\diattenuation.csv')
retardance.to_csv('output\\retardance.csv')
depolarization.to_csv('output\\depolarization.csv')