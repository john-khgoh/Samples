#Standard Scaler implementation that is compatible with SKlearn's pipeline library

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd

class StandardScaler(BaseEstimator,TransformerMixin):
    def __init__(self,*args,**kwargs):
        self.mean = [] #Series means
        self.std = [] #Series standard deviations
        self.signs = None
    
    def fit(self,series):
        #self.series = np.array(series)
        self.series = series
        
        #If series is a list
        if(isinstance(self.series,list)):
            self.mean = np.mean(self.series)
            self.std = np.std(self.series)
            
        #If series is an np.array
        elif(isinstance(self.series,np.ndarray)):
            #Check that it's 2D at most
            dim = self.series.ndim
            if(dim>2):
                raise Exception('Expected 1 or 2 dimensional np.ndarray')
            else:
                #1D np.array
                if(dim==1):
                    self.mean = np.mean(self.series)
                    self.std = np.std(self.series)
                #2D np.array
                else:
                    #Iterate through columns and get column mean and std
                    r,c = np.shape(series)
                    for row in range(r):
                        self.mean.append(np.mean(series[row,:]))
                        self.std.append(np.std(series[row,:]))
                    self.mean = np.expand_dims(np.array(self.mean).transpose(),1)
                    self.std = np.expand_dims(np.array(self.std).transpose(),1)
                    
        #If series is a pd.DataFrame or pd.Series
        elif(isinstance(self.series,(pd.core.frame.DataFrame,pd.core.series.Series))):
            self.mean = list(self.series.mean())
            self.std = list(self.series.std())
        
        return self
    
    def transform(self,series):
        self.series = np.array(series)
        
        div = np.absolute(self.series) + np.float64(1e-12)
        
        #Factorized implementation
        results = self.series-self.mean
        abs_results = abs(results) + np.float64(1e-12)
        self.signs = results/abs_results
        
        results = abs_results/(self.std + np.float64(1e-12))
        return results
          
    def inverse_transform(self,series):
        self.series = np.array(series)
        
        #Factorized implementation
        results = (self.series * self.std * self.signs) + self.mean
        return results


values = [1,2,3,4,5,6,7,8]
price = [2,4,6,8,10,12,14,16]

values = pd.DataFrame({'values':values,'price':price})
#values = np.array([values,price])

test_pipeline = make_pipeline(
    StandardScaler()
)

print(values)
values = test_pipeline.fit_transform(values)
print(values)
values = test_pipeline.inverse_transform(values)
print(values)