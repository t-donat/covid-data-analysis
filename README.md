# covid-data-analysis
Programs and scripts regarding COVID-19 data

## `covid_correlation_analysis.ipynb`

In this Jupyter Notebook file, I took the [COVID-19 case data provided by the Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) and the dataset from the [World Happiness Report](https://www.kaggle.com/unsdsn/world-happiness) provided by the Sustainable Development Solutions Network of the United Nations.

Using these two datasets, I was interested in visualizing what correlation factors such as GDP per capita, healthy life expectancy, generosity or freedom to make life choices have with the average daily COVID-19 cases, deaths and recoveries exhibit. Interestingly enough, both GDP per capita and and healthy life expectancy freedom to make life choices correlated positively with the average number of daily new cases, deaths and recoveries. Howevery, the factor 'generosity' correlated negatively with daily new cases, deaths or recoveries

## `covid_country_data.ipynb`

This .ipynb takes the [same dataset](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) of daily new cases as before, however it graphs the time series of daily new cases. To change the country that is displayed, simply change the string assigned to the variable `country`. There is the option to save the figure using the commented out command.
