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
The second method is the Sharpe model  
The Sharpe model is divided into two dimensions: value and scale  
Therefore, the large-cap growth, large-cap value, mid-cap value, small-cap growth, small-cap value, and a ChinaBond total wealth index index are pulled from the wind as the dividing base.  
A feature of the Sharpe model is that the sum of the weights of each factor must be 1, and this is a linear optimization problem, so the cvx package is used to add linear constraints to solve this optimization problem.   
Both methods use rolling and apply to perform rolling calculations to effectively track changes in fund styles to discover how fund managers adjust positions, what styles are like, and what changes have taken place in styles.  
At the same time, do t test for the generated regression model. If p_value is less than 10%, add an * to the result; if p_value is less than 5%, add two * to the result; if p_value is less than 1%, then Add three * to the result.   

The result of Fama three factor model:  
![image](https://user-images.githubusercontent.com/78793744/117997010-3401a280-b375-11eb-8736-76d52946b704.png)  
![image](https://user-images.githubusercontent.com/78793744/117997097-47147280-b375-11eb-989f-0cb2f8cd1065.png)  
![image](https://user-images.githubusercontent.com/78793744/117997173-54c9f800-b375-11eb-8139-389dd9df0fcf.png)  
The result of Sharpe model:  
![image](https://user-images.githubusercontent.com/78793744/117997287-6b704f00-b375-11eb-81ec-1c383cdf289b.png)  
![image](https://user-images.githubusercontent.com/78793744/117997360-788d3e00-b375-11eb-8dd6-cf062c28bfa4.png)  
![image](https://user-images.githubusercontent.com/78793744/117997422-85aa2d00-b375-11eb-9d27-b184fbe9d11c.png)  

The results are also shown in csv in this assigment.




