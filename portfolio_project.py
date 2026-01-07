#on importe tout les packages 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#la liste les stocks ticker 
stock_list=["AMD","AAPL","MSFT","ORCL"]

#un dictionnaire pour stocker les infos des stocks
stocks_data={}

for i_stock in stock_list:
    stocks_data[i_stock] = pd.read_csv(f"C:/Users/pc/Downloads/{i_stock}.csv", parse_dates=True, index_col="Date")
    
#on peux verifier les premiers 5 lignes de l'un de ses stocks
stocks_data["AMD"]["Adj Close"].head()  

#on calcule le rendement normalisé de chaque stock
for stock_name ,stock_data in stocks_data.items():
    #select the first row of the "Adj Close" column 
    first_adj_close=stock_data.iloc[0]["Adj Close"]
    #Create "Normalized Rerun" column
    stock_data["Normalized Return"]=stock_data["Adj Close"]/first_adj_close
    
#on peux voir un autre stock
stocks_data["AAPL"].head()

#répartir le portefeuille de manière égale entre les actions: equal-weighted portfolio
for stock_name ,stock_data in stocks_data.items():
    
    stock_data["allocation"]=stock_data["Normalized Return"]*0.25
    #0.25 car on a 4 stocks
#on verifie l'un des stocks
stocks_data["AAPL"].head()

#Calculer combien vaut chaque action en dollars dans le portefeuille : position value
for stock_name ,stock_data in stocks_data.items():
    stock_data["Position Value"]=stock_data["allocation"]*10000
    #assuming we have $10,000 to invest in our portfolio (equally weighted across the five stocks and its the value of our entire portfolio)
stocks_data["MSFT"].head()
 
#visualiser la performance du portefeuille en temps reel
position_values = {}

for stock_name  , stock_data in stocks_data.items():
    position_values[stock_name]=stock_data["Position Value"]


position_values=pd.DataFrame(data=position_values)
position_values.head()
#calcule de la valeur total du portefeuille
position_values["Total"]=position_values.sum(axis=1)
position_values.head()
# view the total portfolio
plt.figure(figsize=(12,8))


plt.plot(position_values["Total"])
plt.title("equal-weighted portfolio performance ")
#"Total Portfolio Value Over Time"
plt.xlabel("Date")  
plt.ylabel("Total Portfolio Value (USD)")
#we can see the performance of our equal-weighted portfolio over time
# view the four stocks in the portfolio
plt.figure(figsize=(12,6))

plt.plot(position_values.iloc[:,0:4])
#the first four columns of our data frame which represent the position values for each of the four stocks in our portfolio
plt.title("equal-weighted portfolio stock performance ")
#"Total Portfolio Value Over Time"
plt.xlabel("Date")  
plt.ylabel("Total Portfolio Value (USD)")
#we can see how each of the four stocks  contributed to our portfolio performance
#valeur initial et finale
end_value = position_values["Total"][-1]
start_value=position_values["Total"][0]
#calcule du rendement total
cumulative_returns = (end_value / start_value) - 1
print(f"Cumulative Return: {cumulative_returns}")
#calcule du rendement journaliers
position_values["Daily Returns"] = position_values["Total"].pct_change()
position_values.head()

#calculate the mean Daily Return
mean_daily_return = position_values["Daily Returns"].mean()
print("the mean daily return is:", str(mean_daily_return))
#calcule de la volatilité (écart-type du rendement)
std_daily_return = position_values["Daily Returns"].std()
print("the std daily return is", str(std_daily_return))

# On calcule le sharpe ratio
sharpe_ratio = mean_daily_return / std_daily_return
sharpe_ratio
# Calcule l'annualisation du sharpe ratio
sharpe_ratio_annualized =sharpe_ratio * 252**0.5
sharpe_ratio_annualized
#the sharpe ratio multiplide by the square root of the number of trading days in the year (we are going to assume that they are 252 trading days )
#252:nombre de jours de bourse par an

#On teste sur 10000
stock_adj_close={}
for stock_name , stock_data in stocks_data.items():
    stock_adj_close[stock_name]=stock_data["Adj Close"]
    
stock_adj_close = pd.DataFrame(data=stock_adj_close)
stock_adj_close.head()
# • Create stock returns Dotefrone to see the day over day shonge in seoch value 
stock_returns = stock_adj_close.pct_change()
stock_returns.head()



scenarios = 10000
wheight_array = np.zeros((scenarios , len(stock_returns.columns)))
wheight_array
# Create additional blank arrays for scenario output
returns_array = np.zeros(scenarios)
volatility_array = np.zeros(scenarios)
sharpe_array = np.zeros(scenarios)
# Import the random package and set the seeds
import random
random.seed(3)
np.random.seed(3)
for index in range(scenarios):
 # Generate four random numbers for each index
  numbers = np.array(np.random.random(4))
 # Divide each number by the sun of the numbers to generate the random weight
  wheights = numbers / np.sum(numbers)
 #Save the weights in weights array
  wheight_array[index,:] = wheights
 #calculate the return for each scenario
  returns_array[index] = np.sum(wheights * stock_returns.mean()) * 252
 #calculate the expected volatility for each scenario
  volatility_array[index] = np.sqrt(np.dot(wheights.T, np.dot(stock_returns.cov() * 252, wheights)))

 #calculate the sharpe ratio for each scenario
  sharpe_array[index] = returns_array[index] / volatility_array[index]


print("The first combination:", wheight_array[0])
print("The sharpe ratio of the first portfolio:", sharpe_array[0])



#Identify the Optimal Portfolio
#Now that we have the output for all 10,000 scenarios, we can identify the optimal portfolio. The optimal portfolio in this case study is the portfolio that has the highest sharpe ratio.
# Find the index of the maximum sharpe ratio (the highest charpe ratio in the sharpe_array)
sharpe_array.max()
# Get the index of the optimal portfolio
optimal_index = sharpe_array.argmax()
#index_max_sharpe=optimal_index
optimal_index
#print the optimal weights for each stock
print(stock_list)
print(wheight_array[optimal_index,:])


#Visualize the Optimal Portfolio & Portfolio Scenarios
#Let's visualize our portfolio scenarios by using a scatter chart. We can use the volatility and returns arrays on each axis to see the relationship between risk and reward. As a final step, we can visualize where the optimal portfolio appears among all of the scenarios.
#• Visualize volatility us recurna for each scenario
plt.figure(figsize=(12,8))
plt. scatter (volatility_array, returns_array, c=sharpe_array, cmap="viridis")
plt. colorbar (label="SharpeRatio")
plt.xlabel( "Volatility")
plt.ylabel('Return');

#identify the optimal portfolio in the returns and volatility arrays
max_sharpe_return = returns_array[optimal_index]
max_sharpe_volatility = volatility_array[optimal_index]
#visualize volatility vs returns for each scenario
plt.figure(figsize=(12,8))
plt.scatter(volatility_array, returns_array , c=sharpe_array , cmap= "viridis")
plt.colorbar(label="sharpe ratio")
plt.xlabel("volatility")
plt.ylabel("returns");
#add the optimal portfolio to the visual
plt.scatter(max_sharpe_volatility, max_sharpe_return, c="orange", edgecolors='black')
#edgecolor:add a boarder
#the light colors :high sharp ratio
plt.show()