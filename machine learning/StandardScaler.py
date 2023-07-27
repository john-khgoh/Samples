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
        self.series = np.array(series)
        
        #Check that it's 2D at most
        dim = self.series.ndim
        #print(np.shape(self.series))
        #print('Dimension: %d' %dim)
        if(dim>2):
            raise Exception('Expected 1 or 2 dimensional series (list, numpy.array or pandas.dataframe). Received %d dimensional series.' %(dim))
        else:
            #1D np.array
            if(dim==1):
                self.mean = np.mean(self.series)
                self.std = np.std(self.series)
            #2D np.array
            else:
                #Iterate through columns and get column mean and std
                r,c = np.shape(self.series)
                for col in range(c):
                    self.mean.append(np.mean(self.series[:,col]))
                    self.std.append(np.std(self.series[:,col]))
                    
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


values = [1,2,3,4,5,6,7,8,-1,-2]
price = [2,3,4,5,6,7,8,9,10,11]
values_df = pd.DataFrame({'values':values,'price':price})

test_pipeline = make_pipeline(
    StandardScaler()
)
print(values_df)
values_df = test_pipeline.fit_transform(values_df)
print(values_df)
values_df = test_pipeline.inverse_transform(values_df)
print(values_df)