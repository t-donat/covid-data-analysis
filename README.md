# covid-data-analysis
Programs and scripts to analyze and visualize COVID-19 data

## Covid Dashboard
A dashboard created using plotly and dash that can be run locally. Has an interactive map that can visualize some metrics for a range of different (percentage of pop. that is partially/fully vaccinated, 7 day incidence per 100 000, etc). The dashboard has multiple pages, there are separate pages to plot the time series of (total or daily) infections and vaccination progress. Multiple countries can be selected at the same time and compared with each other. All metrics that are calculated with respect to a population are based on population numbers from 2021 from the UN.

### Setup
First, clone this repository:

``` console
git clone git@github.com:t-donat/covid-data-analysis.git

```

Then, create a virtual environment with a name of your choice. Here, I use conda, but other tools such as venv or virtualenv would work just fine as well. 

``` console
conda create -n <your_environment_name_here>

```

After setting up the environment, activate it:



``` console
conda activate <your_environment_name_here>

```

Then, simply install the required packages using:


``` console
pip install -r requirements.txt

```

### Running the Dashboard
After installation, the dashboard can be launched by simply running the following command:

``` console
python main.py

```

The launcher script will take care of the rest. Launching the dashboard for the first time may take a while, since the population data needs to be downloaded first. After this is completed, a copy is saved locally, so subsequent launches will execute much quicker. Enjoy!



## `covid_correlation_analysis.ipynb` (old)

In this Jupyter Notebook file, I took the [COVID-19 case data provided by the Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) and the dataset from the [World Happiness Report](https://www.kaggle.com/unsdsn/world-happiness) provided by the Sustainable Development Solutions Network of the United Nations.

Using these two datasets, I was interested in visualizing what correlation factors such as GDP per capita, healthy life expectancy, generosity or freedom to make life choices have with the average daily COVID-19 cases, deaths and recoveries exhibit. Interestingly enough, both GDP per capita and and healthy life expectancy freedom to make life choices correlated positively with the average number of daily new cases, deaths and recoveries. Howevery, the factor 'generosity' correlated negatively with daily new cases, deaths or recoveries


## `covid_country_data.ipynb` (old)

This .ipynb takes the [same dataset](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) of daily new cases as before, however it graphs the time series of daily new cases. To change the country that is displayed, simply change the string assigned to the variable `country`. There is the option to save the figure using the commented out command.
