# Business Analysis and launch of AB testing: Targeting Untapped Market

## Insights specific to customers with age group of 18 - 25
# 1. People with age group of 18 -25 accounts to ~25% of customer base in the data
# 2. Avg annual income of this age group is less than 50k
# 3. They don't have much credit history which is getting reflected in their credit score and max credit limit 
# 4. Usage of credit cards as payment type is relatively low compared to other groups
# 5. Avg transaction amount made with credit cards is also low compared to other groups
# 6. Top 3 most used shopping products categories  : Electronics, Fashion & Apparel, Beauty & Personal care


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.stats.api as sms
import statsmodels.api as sm

# finding a sample size to perform testing, we will use power and effect size 
alpha=0.05
power=0.8 # Power is the probability that reject the null hypothesis
effect_size=0.2 # how big the difference is between two group

size=sms.tt_ind_solve_power(
 alpha=alpha,
 power=power,
 effect_size=effect_size,
 alternative="two-sided",
 ratio=1

)

print(size)
# it gives 393 which is a very large sample size it can affect to the budget 
# so we are going to calculate the sample size for different effect size
effect_sizes=[0.1,0.2,0.3,0.4,0.5,1]
for effect_size in effect_sizes:
    sample_size=sms.tt_ind_solve_power(
      alpha=alpha,
      power=power,
      effect_size=effect_size,
      alternative="two-sided",
      ratio=1
    )

    print(f"for effect size : {effect_size} , required sample size is {sample_size:.0f} customer")

# so here we can see that for effect size 0.4 required sample size is 99 which seems to be good as sample size,
# in terms of budgeting also it is good




