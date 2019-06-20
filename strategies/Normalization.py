import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

from .Strategy import Strategy

class Normalization(Strategy):
    Strategy.names.append('Normalization')

    def __init__(self,dfcol):
        super(Strategy, self).__init__()
        self.dfcol=dfcol

    def norm(df,dfcol):
        df[dfcol+'norm']=df[dfcol]/df[dfcol].iloc[0]
        return df
