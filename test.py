import pandas as pd
now = pd.Timestamp.now()
one_year_ago = now - pd.DateOffset(years=1)  # 1年前
two_years_ago = now - pd.DateOffset(years=2)  # 2年前
three_years_ago = now - pd.DateOffset(years=3)  # 3年前

if now>three_years_ago:
    print("未满1年")
else:
    print("满1年以上")