import os
import requests

import altair as alt
import pandas as pd

#
# Settings
#

# Project settings

# project_dir = os.getcwd()
project_dir = os.path.dirname(os.path.realpath(__file__))
print(project_dir)

data_dir = f"{project_dir}/data"
pages_dir = f"{project_dir}/pages"

os.makedirs(data_dir, exist_ok=True)
os.makedirs(pages_dir, exist_ok=True)

# Coronavirus API 
# https://coronavirus.data.gov.uk/details/developers-guide/main-api

api_endpoint = 'https://api.coronavirus.data.gov.uk/v1/data'
metrics = [
    'newCasesByPublishDate', 
    'newCasesBySpecimenDate', 
    # 'newCasesBySpecimenDateAgeDemographics',
    # 'hospitalCases', 'newAdmissions', 'newAdmissionsRollingRate', 
    # 'newDeathsByDeathDate', 'newDeaths28DaysByDeathDate',
    # 'newDeaths28DaysByDeathDateAgeDemographics',
    # 'newPeopleReceivingFirstDose',
    # 'vaccinationsAgeDemographics'
    ]
columns = ['date'] + metrics
request_url = f'{api_endpoint}?format=csv&filters=areaType=ltla;areaName=Lewisham&structure=["' + '","'.join(columns) + '"]'
print(request_url)

# Chart settings
width = 500
height = 300

#
# Get the data
#

response = requests.get(request_url, timeout=10)

if response.status_code >= 400:
    raise RuntimeError(f'Request failed: { response.text }')

# Write to local cache
with open(f"{data_dir}/data.csv", 'w') as f:
    f.write(response.text)
    print(response.text[:256] + '...')

#
# Prepare the data
#

data = pd.read_csv(f"{data_dir}/data.csv")

# Only show the last year
chart_data = data.head(356)

# Drop unused columns to keep file sizes small
chart_data = data[columns]

#
# Make the chart
#

chart = alt.Chart(chart_data).transform_fold(
    metrics
).mark_line().encode(
    x='date:T',
    y='value:Q',
    color=alt.Color('key:N', legend=alt.Legend(
        orient="top-left",
        title=None))
).properties(
    width=width,
    height=height
)

chart.save(f"{pages_dir}/index.html")
