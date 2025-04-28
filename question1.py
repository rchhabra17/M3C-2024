import pandas as pd
from statsmodels.tsa.api import VAR
import numpy as np
import matplotlib.pyplot as plt

mortgage_raw = pd.read_csv('mortgage_rate.csv')
mortgage_adj = mortgage_raw.iloc[::12].reset_index()

pop_seattle = pd.read_csv('population_seattle.csv')
inc_seattle = pd.read_csv('income_seattle.csv')
house_seattle = pd.read_csv('housing_seattle.csv')

df = pd.DataFrame()
df["Housing Units"] = list(map(float,house_seattle["Housing Units"]))
df["Mortgage Rate"] = mortgage_adj["MORTGAGE30US"]
# df["Household Income"] = list(map(float,inc_seattle["MHIWA53033A052NCEN"]))
df["Population"] = pop_seattle["WAKING5POP"]*1000
df.drop([10,11,12],inplace=True)
print(df)


endog = df[['Housing Units',"Mortgage Rate",'Population']]

model = VAR(endog)
model_fit = model.fit()

lag_order = model_fit.k_ar
pred = model_fit.forecast(endog.values[-lag_order:], 50)
model_fit.plot_forecast(10)
# print(f"The predicted housing supply is {prediction['Housing Units'].values[0]}")

forecasted_housing_units = pred[:, 0]  # Assuming housing units is the first variable in your endogenous variables

# Generate years for the forecasted period

# Plot the original housing units data along with the forecasted values
plt.figure(figsize=(10, 6))
plt.plot(house_seattle["Year"].drop([10,11,12]), df["Housing Units"], label="Actual Housing Units")
plt.plot([i for i in range(2023,2073)], forecasted_housing_units, label="Forecasted Housing Units")
plt.xlabel("Year")
plt.ylabel("Housing Units")
plt.title("Forecasted Housing Units for Next 50 Years")
plt.legend()
plt.grid(True)
plt.show()