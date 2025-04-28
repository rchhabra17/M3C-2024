import pandas as pd
from statsmodels.tsa.api import VAR
import numpy as np
import matplotlib.pyplot as plt

mortgage_raw = pd.read_csv('mortgage_rate.csv')
mortgage_adj = mortgage_raw.iloc[::12].reset_index()

home_seattle = pd.read_csv('homelessness_seattle.csv')
price_seattle = pd.read_csv('median_price_seattle.csv')
house_seattle = pd.read_csv('housing_seattle2.csv')
pop_seattle = pd.read_csv('population_seattle1.csv')

df = pd.DataFrame(pop_seattle["Year"])
df["Total Homeless"] = list(map(float,home_seattle["Homeless Total"]))
df["Ratio of Required Income for House Finacing to Actual Income"] = price_seattle["Compare to 30%"]
df["Housing Units"] = house_seattle["Vacant units"]
df["Prop Homeless"] = home_seattle["Proportion Homelessness"]
df['Mortgage Rate'] = price_seattle["Mortage Rate"]
df["Population"] = pop_seattle["Total Population"]


#df.drop([10,11,12],inplace=True)
print(df)


endog = df[["Total Homeless",'Ratio of Required Income for House Finacing to Actual Income','Population']]
#endog = endog.diff().dropna()
#exog = df['Population']
#test for stationarity
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def adf_test(series, name=''):
    result = adfuller(series, autolag='AIC')
    print(f'ADF Test for {name}:')
    print('Test Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:', result[4])
    print('Is the time series stationary?', 'No (reject null hypothesis)' if result[1] < 0.05 else 'Yes (fail to reject null hypothesis)')
    print('\n')

# Apply ADF test to each variable
for column in endog.columns:
    adf_test(endog[column], name=column)
    
#Test for cointegration
#Test for cointegration   
import statsmodels.api as sm

y = df['Total Homeless']
X = df[['Ratio of Required Income for House Finacing to Actual Income','Mortgage Rate']]
X = sm.add_constant(X)

model = sm.OLS(y, X)
results = model.fit()

residuals = results.resid
adf_test(residuals, name='Residuals')

#build the VAR
model = VAR(endog)
model_fit = model.fit()

lag_order = model_fit.k_ar
pred = model_fit.forecast(endog.values[-lag_order:], 50)
model_fit.plot_forecast(50)
#print(f"The predicted housing supply is {pred['Housing Units'].values[0]}")
print(f"Predicted: {pred}")

forecasted_housing_units = pred[:, 0]  # Assuming housing units is the first variable in your endogenous variables
#forecasted_housing_units = forecasted_housing_units.cumsum()
print(f"Forecasted : {forecasted_housing_units[-1]}")
# Generate years for the forecasted period
forecasted_years = np.arange(df["Year"].max()+1, df["Year"].max() + 51)
print(forecasted_housing_units)

# Plot the original housing units data along with the forecasted values
plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df["Total Homeless"], label="Homeless Population Actual")
plt.plot(forecasted_years, forecasted_housing_units, label="Forecasted Homeless Population")
plt.xlabel("Year")
plt.ylabel("Homeless Population")
plt.title("Forecasted Homeless Population for Next 50 Years")
plt.legend()
plt.grid(True)
plt.show()

