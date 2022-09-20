#include everything from loader
from loader import *
cleanlist = []

#the following process is a loop that saves on the list called "cleanlist" a group of lists made of lists
#there's one for each reporter on the list called "countries"
#each one of theese "list lists" has four elements:
# 1) The name of the reporter the data refers to
# 2) The year operation were made in
# 3) The FOB value of the operation
# 4) The first trading parter of the operation

for c in range(len(countries)):

    ylist = []
    flist = []
    countrylist = []
    plist = []

    for l in range(len(main_data)):
        if main_data.at[l,'ReporterDesc'] == countries[c]:
            ylist.append(main_data.at[l, 'RefYear'])
            flist.append(main_data.at[l,'Fobvalue'])
            plist.append(main_data.at[l, 'PartnerDesc'])
        countrylist.append(countries[c])
        countrylist.append(ylist)
        countrylist.append(flist)
        countrylist.append(plist)
    cleanlist.append(countrylist)

#follow to the dfgenerator file
