import pandas as pd

main_data=pd.read_csv(r"C:\Users\User\Desktop\EstDev\TradeData.csv")

#getting the individual reporters using unique method
countries = main_data.ReporterDesc.unique()
#follow to the writer.py file
years = main_data['RefYear'].unique()
print(years)