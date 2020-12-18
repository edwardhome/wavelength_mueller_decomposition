import numpy as np
import math 

def sqrt(num):
    return num**0.5
min=float(2.2250738585072014**-308)

class Mueller:
    def __init__(self):
        self.MuellerMatrix = np.empty([4,4],dtype=float)
    def mueller(self,I1=0.5,I2=0.5,I3=0.716506351,I4=0.283493649,I5=0.375,I6=0.066987298,I7=0.625,I8=0.625,I9=0.066987298,I10=0.375,I11=0,I12=0.5,I13=1,I14=0.5,I15=1,I16=0.5):
        N1=I14+I16+(2*(I5+I7+I8+I10)-(I11+I13+3*I14+3*I16))/(2*sqrt(3)+3)
        M1=N1/N1
        M2=(2*(I8+I10-I5-I7)/sqrt(3))/N1
        M3=(I14+I16-I11-I13+(2*(I5+I7+I8+I10)-(I11+I13+3*I14+3*I16))/(2*sqrt(3)+3))/N1
        M4=((2*(I5+I7+I8+I10)-(I11+I13+3*I14+3*I16))/(2*sqrt(3)+3))/N1
        M5=(2*I1-I14-I16+(-6*I1-2*I2+4*I3+4*I4-2*I5-2*I7-2*I8-2*I10+I11+I13+3*I14+3*I16)/(2*sqrt(3)+3))/N1
        M6=(2*(2*I3+I5+I7-2*I4-I8-I10)/sqrt(3))/N1
        M7=(2*I1-2*I2+I11+I13-I14-I16+(-6*I1-2*I2+4*I3+4*I4-2*I5-2*I7-2*I8-2*I10+I11+I13+3*I14+3*I16)/(2*sqrt(3)+3))/N1
        M8=((-6*I1-2*I2+4*I3+4*I4-2*I5-2*I7-2*I8-2*I10+I11+I13+3*I14+3*I16)/(2*sqrt(3)+3))/N1
        M9=(I16-I14+(2*I5+2*I10+I13+3*I14-2*I7-2*I8-I11-3*I16)/(2*sqrt(3)+3))/N1
        M10=(2*(I7+I10-I5-I8)/sqrt(3))/N1
        M11=(I13+I16-I11-I14+(2*I5+2*I10+I13+3*I14-2*I7-2*I8-I11-3*I16)/(2*sqrt(3)+3))/N1
        M12=((2*I5+2*I10+I13+3*I14-2*I7-2*I8-I11-3*I16)/(2*sqrt(3)+3))/N1
        M13=(I14+I16-2*I15+(2*I5+2*I7+2*I8+2*I10+2*I12+6*I15-4*I6-4*I9-I11-I13-3*I14-3*I16)/(2*sqrt(3)+3))/N1
        M14=(2*(2*I6+I8+I10-I5-I7-2*I9)/sqrt(3))/N1
        M15=(I14+I16-I11-I13+2*I12-2*I15+(2*I5+2*I7+2*I8+2*I10+2*I12+6*I15-4*I6-4*I9-I11-I13-3*I14-3*I16)/(2*sqrt(3)+3))/N1
        M16=((2*I5+2*I7+2*I8+2*I10+2*I12+6*I15-4*I6-4*I9-I11-I13-3*I14-3*I16)/(2*sqrt(3)+3))/N1
        self.MuellerMatrix = np.array([[M1,M2,M3,M4],[M5,M6,M7,M8],[M9,M10,M11,M12],[M13,M14,M15,M16]],dtype=float)-min
        return self.MuellerMatrix
class Luchiman(Mueller):
    def __init__(self,MuellerMatrix):
        super().__init__()
        self.diattenuationMatrix = np.empty([4,4],dtype=float)
        self.MuellerMatrix = MuellerMatrix
    def diattenuation(self,output):
        #雙衰減矩陣計算
        self.D_value = sqrt(self.MuellerMatrix[0,1]**2+self.MuellerMatrix[0,2]**2+self.MuellerMatrix[0,3]**2)#衰減係數
        self.D_vector = np.array([self.MuellerMatrix[0,1],self.MuellerMatrix[0,2],self.MuellerMatrix[0,3]])
        self.P_value = sqrt(self.MuellerMatrix[1,0]**2+self.MuellerMatrix[2,0]**2+self.MuellerMatrix[3,0]**2)#極化能力
        self.P_vector = np.array([self.MuellerMatrix[1,0],self.MuellerMatrix[2,0],self.MuellerMatrix[3,0]])
        mD = np.array(sqrt(1-(self.D_value)**2)*np.eye(3)+(1-sqrt(1-(self.D_value)**2))*((self.D_vector.dot(self.D_vector.T))/self.D_value),dtype=float)
        self.diattenuationMatrix[0] = np.array([1,self.MuellerMatrix[0,1],self.MuellerMatrix[0,2],self.MuellerMatrix[0,3]])
        self.diattenuationMatrix[1:4,0] = np.array([self.MuellerMatrix[0,1],self.MuellerMatrix[0,2],self.MuellerMatrix[0,3]])
        self.diattenuationMatrix[1:4,1:4] = np.array(mD)
        self.D_h = self.diattenuationMatrix[0,1]
        self.D_45 = self.diattenuationMatrix[0,2]
        self.D_c = self.diattenuationMatrix[0,3]
        self.D_L = sqrt(self.D_45**2+self.D_h**2)
        self.doubleTheta = (0.5*math.atan(abs(self.D_45)/abs(self.D_h)))*math.pi/180
        if output == 'D_value':
            return self.D_value
        elif output == 'P_value':
            return self.P_value
        elif output == 'matrix':
            return self.diattenuationMatrix
        elif output =='D_H':
            return self.D_h
        elif output =='D_45':
            return self.D_45
        elif output =='D_C':
            return self.D_c
        elif output =='D_L':
            return self.D_L
        elif output =='doubleTheta':
            return self.doubleTheta
        else:
            print('雙衰減係數計算輸出指令錯誤')

    def depolarization(self,output):
        #去極化矩陣計算
        try:
            dm_prime = np.linalg.inv(self.diattenuationMatrix)
        except:
            dm_prime = np.eye(4)
        self.MuellerMatrix_prime = self.MuellerMatrix.dot(dm_prime)
        m_prime = self.MuellerMatrix_prime[1:4,1:4]
        P_delta_vector = self.MuellerMatrix_prime[1:4,0]
        mm = m_prime.dot(m_prime.T) # 轉置矩陣相乘
        try:
            eigenvalues = np.linalg.eigvals(mm) #取特徵值
        except:
            eigenvalues = np.array([1,1,1])
        fa = np.linalg.inv(mm+(sqrt(eigenvalues[0]*eigenvalues[1])+(sqrt(eigenvalues[1]*eigenvalues[2])+(sqrt(eigenvalues[2]*eigenvalues[0]))))*np.eye(3))
        fb = ((sqrt(eigenvalues[0])+sqrt(eigenvalues[1])+sqrt(eigenvalues[2]))*mm+(sqrt(eigenvalues[0]*eigenvalues[1]*eigenvalues[2])*np.eye(3)))
        m_delta =fa.dot(fb)
        self.depolarizationMatrix = np.empty([4,4],dtype= float)
        self.depolarizationMatrix[0] = [1,0,0,0]
        self.depolarizationMatrix[1:4,0] = P_delta_vector
        self.depolarizationMatrix[1:4,1:4] = m_delta
        Delta_value = 1-abs((np.trace(self.depolarizationMatrix)-1)/3)
        if output == 'Delta_value':
            return Delta_value
        elif output == 'matrix':
            return self.depolarizationMatrix
        else:
            print('去極化計算輸出指令錯誤')

    def retardance(self,output):
        #相位延遲矩陣計算
        try:
            A = np.linalg.inv(self.depolarizationMatrix)
        except:
            A = np.eye(4)
        B = self.MuellerMatrix_prime
        self.retardanceMatrix = A.dot(B)
        try:
            self.R_value = math.acos(np.trace(self.retardanceMatrix)/2-1)
        except:
            self.R_value = math.acos(4/2-1)
        if output == 'matrix':
            return self.retardanceMatrix
        else:
            print('相位延遲計算輸出指令錯誤')

    def retardancevalue(self,output,Otype='D'):
        linearretardance_value = math.acos(sqrt((self.retardanceMatrix[1,1]+self.retardanceMatrix[2,2])**2+(self.retardanceMatrix[1,2]+self.retardanceMatrix[2,1])**2)-1)
        opticalactivity_value = math.atan((self.retardanceMatrix[1,2]-self.retardanceMatrix[2,1])/(self.retardanceMatrix[1,1]+self.retardanceMatrix[2,2]))
        r2 = (1/(2*math.sin(self.R_value)+min))*(self.retardanceMatrix[3,1]-self.retardanceMatrix[1,3])
        r3 = (1/(2*math.sin(self.R_value)+min))*(self.retardanceMatrix[1,2]-self.retardanceMatrix[2,1])
        theta_value = 0.5*math.atan((r3/r2))#需驗證
        if Otype == 'D':
            if output == 'linear':
                return linearretardance_value*180/math.pi
            elif output == 'R_value':
                return self.R_value*180/math.pi
            elif output == 'opticalactivity':
                return opticalactivity_value*180/math.pi
            elif output == 'theta':
                return theta_value*180/math.pi
            else:
                print('請確認延遲量參數')
        elif Otype == 'R':
            if output == 'linear':
                return linearretardance_value
            elif output == 'self.R_value':
                return self.R_value
            elif output == 'opticalactivity':
                return opticalactivity_value
            elif output == 'theta':
                return theta_value
            else:
                print('請確認延遲量參數')
        else:
            print('請選擇輸出弳度或度度量')
class Differential(Mueller):
    def __init__(self,MuellerMatrix):
        super().__init__()
        self.MuellerMatrix = MuellerMatrix
        