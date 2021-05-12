# Assignment3
This assignment mainly focuses on fund evaluation   
Two methods are used to evaluate the fund first.  
The first method is the Fama three-factor model：  
The Fama three-factor model is mainly based on the market value and book market value to do regression.  
The market value is the return of the large-cap stock minus the return of the small-cap stock, and the book value ratio is the low-book ratio minus the return of the high-book ratio portfolio.  
Therefore, we select the Giant Tide Small Cap Index, the Giant Tide Large Market Index, the Giant Tide Growth Index and the Giant Tide Value Index as the basis for dividing funds.  
Among them, the SMB factor is the return rate of the Giant Tide Small Cap Index minus the return rate of the Giant Tide Large Cap Index.  
At the same time, the Fama three factors also have a market portfolio yield minus the risk-free interest rate factor.  
This factor is replaced by Wind Quan A Index.  
After obtaining the SMB and HML and the market factor, I use the OLS of statsmodel to calculate, but the cvx package is used in the code to calculate. This is because there are constraints in the solution of the subsequent Sharpe model, and ordinary OLS cannot solve the constrained Optimization problem.   
