#Scatter plot of material cost vs strength using Plotly express

import plotly.express as px
import pandas as pd
from os import getcwd

wd = getcwd()
file = wd + "\\Materials Cost vs Strength.xlsx"
df = pd.read_excel(file,sheet_name="Sheet2")
#Filter out materials that cost more than $10/kg
df = df[df["Cost"]<=10]
fig = px.scatter_3d(df,x="Cost",y="Density",z="Young's Modulus",hover_data=["Material"],color="Type")
fig.show()