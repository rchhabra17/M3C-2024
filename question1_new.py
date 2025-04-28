import numpy as np
import pmdarima as ar
import matplotlib.pyplot as plt
import pandas as pd



data = pd.read_csv("housing_seattle_new.csv")
for i in range(50):
   data = data.append({"Year":2022+i, "Housing Units":0},ignore_index=True)

data.set_index("Year",inplace=True)
data.plot()


# Train and Test Value
train = data[:13]
print(train)
test = data[-50:]
plt.plot(train)
plt.plot(test)

arima_model = ar.auto_arima(train,start_p=0,d=1,start_q=0,max_p=5,max_d=5,max_q=5,start_P=0,D=1,start_Q=0,max_P=5,max_D=5,max_Q=5,m=12,
seasonal=True,error_action='warn',trace=True,suppress_warnings=True,stepwise=True,random_state=20,n_fits=50)


arima_model.summary()

prediction = pd.DataFrame(arima_model.predict(n_periods=50),index=test.index)
prediction.columns = ['Predicted Housing Units']
print(prediction)


# Values for Year
print(prediction.iloc[[10]])
print(prediction.iloc[[20]])
print(prediction.iloc[[50]])

