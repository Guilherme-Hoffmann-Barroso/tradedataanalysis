from writer import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#since I want to modify certain dataframes using info from themselves, I apparently have to tell pandas to let me do so
pd.set_option('chained_assignment', None)

#now, we will create one csv file for each of the reporters, containing three collums:
# 1) The year operation were made in
# 2) The FOB value of the operation
# 3) The first trading parter of the operation
#this will be done in order to:
# 1) Load the new files into separate dataframes
# 2) Use them to get the total value of the operations with trading partners within and without the EU
#we will late use this information to plot the desired graphs

xlswriter = pd.ExcelWriter('estentregacomt.xlsx', engine='xlsxwriter')

for i in range(len(countries)):
    tdf = pd.DataFrame(columns=('Year', 'Partner', 'FOBvalue', 'FOBw'))
    tdf4 = pd.DataFrame(columns=('Year', 'Intra Block exp.', 'Extra Block exp.'))
    tdf['Year'] = cleanlist[i][1]
    tdf['FOBvalue'] = cleanlist[i][2]
    tdf['Partner'] = cleanlist[i][3]
    for z in range(len(tdf['FOBvalue'])):
        if tdf['Partner'].iloc[z] in countries:
            tdf['FOBw'].iloc[z] = tdf['FOBvalue'].iloc[z]
    tdf.to_csv(fr'C:\Users\User\Desktop\EstDev\{countries[i]}.csv', sep = ';')
    tdf2 = tdf.groupby('Year').sum()
    tdf2.to_csv(fr'C:\Users\User\Desktop\EstDev\{countries[i]}_grouped.csv', sep=';')
    tdf3 = tdf.groupby('Year')['FOBw'].sum()
    tdf3.to_csv(fr'C:\Users\User\Desktop\EstDev\{countries[i]}_grouped_internal.csv', sep=';')
    #I have to convert tdf3 into a dataframe (it is currently a series) in oderder to work with it
    tdf3= tdf3.to_frame()

    #tdf2.to_excel(xlswriter, sheet_name=f"{countries[i]}grouped_ext")
    #tdf3.to_excel(xlswriter, sheet_name=f"{countries[i]}grouped_int")

    # now, to grate stacked bar plots for every country
    # I was getting a type error trying to use numpy to subtract arrays directly from the temporary data frames
    # So I will convert the rows to numeric by casting them to series, and then converting them using the to_numeric method
    # There may be a easier way to do this, but I couldn't find any
    ser1 = pd.Series(tdf2['FOBvalue'])
    ser2 = pd.Series(tdf3['FOBw'])

    exports = pd.to_numeric(ser1)
    intexports = pd.to_numeric(ser2)
    Exports = np.array(exports)
    Internalexp = np.array(intexports)
    Externalexports = np.subtract(Exports, Internalexp)

    max = np.max(Internalexp) + np.max(Externalexports)
    print(f"IE{len(Internalexp)}")
    print(f"EI{len(Externalexports)}")
    print(f"Y{len(years)}")

    if len(Internalexp) == len(years):
        EG = plt.bar(years, Externalexports, color='r')
        IG = plt.bar(years, Internalexp, color='b', bottom=Externalexports)
        plt.xlabel("Years")
        plt.ylabel("Total exports")
        plt.ylim(0, max)
        plt.legend([EG,IG], ['exports to countries outside the EU', 'exports to countries within the EU'])
        plt.title(f"Exports from {countries[i]}, as reported by Comtrade")
        plt.savefig(f'{countries[i]}_graph.png')
        tdf4['Year'] = years
        tdf4['Intra Block exp.'] = Internalexp
        tdf4['Extra Block exp.'] = Externalexports
        tdf4.to_excel(xlswriter, sheet_name=f"{countries[i]}")


    else:
        print(f"value error in country {countries[i]}")

xlswriter.save()