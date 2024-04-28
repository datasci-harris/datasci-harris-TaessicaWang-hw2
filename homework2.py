"""
Write your answers in the space between the questions, and commit/push only
this file (homework2.py) and countries.csv to your repo. Note that there can 
be a difference between giving a "minimally" right answer, 
and a really good answer, so it can pay to put thought into your work. 

This is a much longer project than those you've done in class - remember to use
comments to help readers navigate your work!

To answer these questions, you will use the two csv files provided in the repo.
The file named gdp.csv contains the per capita GDP of many countries in and 
around Europe in 2023 US dollars. The file named population.csv contains 
estimates of the population of many countries.
"""

"""
QUESTION 1

Short: Open the data

Long: Load the GDP data into a dataframe. Specify an absolute path using the Python 
os library to join filenames, so that anyone who clones your homework repo 
only needs to update one string for all loading to work.
"""
import pandas as pd
base_path= "/Users/taessica/Documents/GitHub/datasci-harris-TaessicaWang-hw2"

import os
path = os.path.join(base_path,"gdp.csv")
df_gdp= pd.read_csv(path)
print(path)


"""
QUESTION 2

Short: Clean the data

Long: There are numerous issues with the data, on account of it having been 
haphazardly assembled from an online table. To start with, the column containing
country names has been labeled TIME. Fix this.

Next, trim this down to only member states of the European Union. To do this, 
find a list of members states (hint: there are 27 as of Apr 2024) and manually 
create your own CSV file with this list. Name this file countries.csv. Load it 
into a dataframe. Merge the two dataframes and keep only those rows with a 
match.

(Hint: This process should also flag the two errors in naming in gdp.csv. One 
 country has a dated name. Another is simply misspelt. Correct these.)
"""
import pandas as pd
df_gdp.rename(columns = {'TIME': 'Country'}, inplace=True)

# correct naing errors
df_gdp['Country'] = df_gdp['Country'].replace({'Czechia': 'Czech Republic', 'Itly': 'Italy'})

eu_countries = [
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 
    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 
    'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 
    'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 
    'Slovenia', 'Spain', 'Sweden'
]

# Create a DataFrame for EU countries
df_eu_countries = pd.DataFrame(eu_countries, columns= ['Country'])
csv_path = "/Users/taessica/Documents/GitHub/datasci-harris-TaessicaWang-hw2/countries.csv"
df_eu_countries.to_csv(csv_path, index=False)
print("Countries.csv has been created at:", csv_path)

# Merge GDP data with EU countries
df_filtered_gdp = pd.merge(df_gdp, df_eu_countries, on='Country')
print(df_filtered_gdp.head())


"""
QUESTION 3

Short: Reshape the data

Long: Convert this wide data into long data with columns named year and gdp.
The year column should contain int datatype objects.

Remember to convert GDP from string to float. (Hint: the data uses ":" instead
of NaN to denote missing values. You will have to fix this first.) 
"""
# Replace ":" with NaN for missing values
df_gdp.replace(":", pd.NA, inplace=True)

df_long = df_gdp.melt(id_vars='Country', var_name='year', value_name='gdp')
df_long['year'] = df_long['year'].str.extract('(\d+)').astype(int)
df_long['gdp'] = pd.to_numeric(df_long['gdp'], errors='coerce')

print(df_long.head())


"""
QUESTION 4

Short: Repeat this process for the population data.

Long: Load population.csv into a dataframe. Rename the TIME columns. 
Merge it with the dataframe loaded from countries.csv. Make it long, naming
the resulting columns year and population. Convert population and year into int.
"""
import pandas as pd
df_population = pd.read_csv('/Users/taessica/Documents/GitHub/datasci-harris-TaessicaWang-hw2/population.csv')
df_population.rename(columns={'TIME': 'Country'}, inplace=True)
df_eu_countries = pd.read_csv('/Users/taessica/Documents/GitHub/datasci-harris-TaessicaWang-hw2/countries.csv')

df_merged = pd.merge(df_population, df_eu_countries, on='Country')

df_long2 = df_merged.melt(id_vars='Country', var_name='year', value_name='population')
# Extracting the numeric part of the 'year' and convert to int
df_long2['year'] = df_long2['year'].str.extract('(\d+)').astype(int)
# Convert 'population' to int, fixing non-numeric issues
df_long2['population'] = pd.to_numeric(df_long2['population'], errors='coerce').fillna(0).astype(int)

print(df_long2.head())


"""
QUESTION 5

Short: Merge the two dataframe, find the total GDP

Long: Merge the two dataframes. Total GDP is per capita GDP times the 
population.
"""
df_merged = pd.merge(df_long, df_long2, on=['Country', 'year'])
# Calculate total GDP by multiplying GDP per capita with population
df_merged['total_gdp'] = df_merged['gdp'] * df_merged['population']
print(df_merged.head())


"""
QUESTION 6

Short: For each country, find the annual GDP growth rate in percentage points.
Round down to 2 digits.

Long: Sort the data by name, and then year. You can now use a variety of methods
to get the gdp growth rate, and we'll suggest one here: 

1. Use groupby and shift(1) to create a column containing total GDP from the
previous year. We haven't covered shift in class, so you'll need to look
this method up. Using groupby has the benefit of automatically generating a
missing value for 2012; if you don't do this, you'll need to ensure that you
replace all 2012 values with missing values.

2. Use the following arithematic operation to get the growth rate:
    gdp_growth = (total_gdp - total_gdp_previous_year) * 100 / total_gdp
"""
import pandas as pd
# Sort the data by 'Country' and 'year'
df_merged_sorted = df_merged.sort_values(by=['Country', 'year'])
df_merged_sorted['total_gdp_previous_year'] = df_merged_sorted.groupby('Country')['total_gdp'].shift(1)

# Calculate the GDP growth rate
df_merged_sorted['gdp_growth'] = (
    df_merged_sorted['total_gdp'] - df_merged_sorted['total_gdp_previous_year']
    ) * 100 / df_merged_sorted['total_gdp']
df_merged_sorted.dropna(subset=['gdp_growth'], inplace=True)
# Round the growth rate to two decimal places
df_merged_sorted['gdp_growth'] = df_merged_sorted['gdp_growth'].round(2)

print(df_merged_sorted[['Country', 'year', 'gdp_growth']].head())


"""
QUESTION 7

Short: Which country has the highest total gdp (for the any year) in the EU? 

Long: Do not hardcode your answer! You will have to put the automate putting 
the name of the country into a string called country_name and using the following
format string to display it:

print(f"The largest country in the EU is {country_name}")
"""
# Find the row with the highest total GDP
largest_gdp_row = df_merged.loc[df_merged['total_gdp'].idxmax()]
# Extract the country name from this row
country_name = largest_gdp_row['Country']
print(f"The largest country in the EU is {country_name}")


"""
QUESTION 8

Create a dataframe that consists only of the country you found in Question 7

In which year did this country have the most growth in the period 2012-23?

In which year did this country have the least growth in the peroid 2012-23?

Do not hardcode your answer. You will have to use the following format strings 
to show your answer:

print(f"Their best year was {best_year}")
print(f"Their worst year was {worst_year}")
"""
import pandas as pd
country_data = df_merged_sorted[df_merged_sorted['Country'] == country_name]
# Filter for the years 2012 to 2023
country_data = country_data[(country_data['year'] >= 2012) & (country_data['year'] <= 2023)]
# Find the year with the maximum and minimum GDP growth
best_year = country_data.loc[country_data['gdp_growth'].idxmax(), 'year']
worst_year = country_data.loc[country_data['gdp_growth'].idxmin(), 'year']
print(f"Their best year was {best_year}")
print(f"Their worst year was {worst_year}")





