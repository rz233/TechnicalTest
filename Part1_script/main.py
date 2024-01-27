from datetime import datetime
import os
import pandas as pd
from functions import *
import plotly
import plotly.express as px




if __name__ == '__main__':

    # create the output path, please change it to your own local path!!!!!!!!!!!!
    #outputs_path = '/PATH/TO/OUTPUT/FOLDER/'
    outputs_path = '/Users/ruiwenzhang/Documents/ETC_tech_test/updated_part1'


    ## Step 1: Pull the data from API -------------------------------------------
    # Data URL
    data_url = 'http://api.worldbank.org/v2/country/all/indicator/SH.STA.BASS.ZS'
    # additional parameters required for the API request
    params = {
        'per_page': 1000,
        'format': 'json'
    }

    # Fetch all data
    full_dataset = fetch_all_pages(data_url, params)
    # print("Total items fetched:", full_dataset)
    print("Total items fetched:", len(full_dataset))

    # Flat data because some json fields are nested objects
    flattened_data = [flatten_data(item) for item in full_dataset]
    print("Total items flattened_data:", flattened_data)
    print("Total items flattened_data:", len(flattened_data))

    # Write raw data to the outputs path
    csv_file = os.path.join(outputs_path, "raw_data.csv")
    write_to_file(csv_file, flattened_data)
    print(f"Raw Data written to {csv_file}")



    ## Step 2: Conduct simple exploratory analysis and clean the raw data -------------------------------------
    # check unique value in Unit, obs_status, decimal columns because it seems to be not helpful for the data visualization
    verifyData(flattened_data)

    # read the raw data csv file into pandas dataframe
    raw_data = pd.read_csv(csv_file)
    # remove columns that are not relevant to the final visualization
    keep_cols = ['country.value', 'countryiso3code', 'date', 'value']
    clean_data = raw_data[keep_cols]

    # remove data where the value is null
    clean_data = clean_data.dropna(subset=['value'])

    # rename date column as year
    clean_data = clean_data.rename({'date':'year'}, axis = 1)

    # clean_data by region and by income group
    print(clean_data['country.value'].unique())

    region = ['East Asia & Pacific', 'Europe & Central Asia',
    'Latin America & Caribbean', 'Middle East & North Africa',
    'North America', 'South Asia', 'Sub-Saharan Africa' ]

    income_group = ['Low income', 'Lower middle income', 
    'Upper middle income', 'High income']

    clean_data_region = clean_data[clean_data['country.value'].isin(region)].\
        sort_values('year').\
        rename({'country.value': 'region'}, axis = 1)
    clean_data_income = clean_data[clean_data['country.value'].isin(income_group)].\
        sort_values('year').\
        rename({'country.value': 'income group'}, axis = 1)




    # Write clean data to the outputs path
    csv_file_clean = os.path.join(outputs_path, "clean_data.csv")
    clean_data.to_csv(csv_file_clean, index = False)

    clean_data_region.to_csv("clean_data_reg.csv",index=False)
    clean_data_income.to_csv("clean_data_income.csv",index=False)
    #write_to_file(csv_file_clean, clean_data)
    #print(f"Clean Data written to {csv_file_clean}")


    ## Step 3: create a chart ----------------------------------------------------
    fig = px.line(clean_data_region, x="year", y="value", color='region')
    fig.add_traces(px.scatter(clean_data_income, x="year", y="value", size="value",color="income group").data)
    fig.update_layout(title = 0.5)
    fig.update_layout(title_text = "People using at least basic sanitation services (% of population) by Region and by Income Group")
    div = plotly.offline.plot(fig, include_plotlyjs=False, output_type = 'div')
    #fig.show()

 

    # the html code which will go in the file part1_output.html 
    html_template = '''<html> 
    <head> <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>Title</title> 
    </head> 
    <body> 
    <h2> Part 1  Output</h2> 
    <h3>1. Finding </h3> 
    <p>We can see that starting from the year of 2000, the % of population using at least basic sanitation services goes up 
    in all regions except the North America region. Sub-Saharan Africa region has the lowest % population starting from 2023. 
    The % population in North America is near 100% from 2000 and 2020.
    If we looking at the % population by income group, % population rises over time for all income group except the high income group.
    No surprise that the low income group has the lowest % population </p> 

    <h3>2. Approach </h3> 

    <p>Since we need to show the trend over time, the best chart type would be line chart so I choose to use 
    line chart to visualize the data. Since we want to look at the trend, from my perspective, showing data by region is a
    good option as plotting all countries data would make the figure so messy and not organized.
    Then I differenciate data by using different color for each region. Also we need to
    show the data by income group, I differentiate them by using different color and bubble size for each income group. 
    In addition, the interactive visualization could provide user with more clear data.
    </p> 

    <h3>3. Visualization</h3> 
    '''+ div + ''' 

 
  
    </body> 
    </html> 
    '''
  
# writing the code into the file 
with open('Part1_output.html', 'w') as f:
    f.write(html_template) 
  
# close the file 
    f.close() 

   