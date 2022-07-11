import os
from operator import itemgetter
from collections import OrderedDict

import pandas as pd

from covid_dashboard.utils import change_date_format_to_dmy, format_date_string


def load_population_data(population_url, countries_of_best):

    target_filepath = os.path.join(os.path.dirname(__file__),
                                   "config",
                                   "populations_of_best_countries.csv")

    # print(target_filepath)

    if os.path.exists(target_filepath):
        return pd.read_csv(target_filepath, index_col="Location")

    else:
        population_data = pd.read_csv(population_url)

        reduced_popuation_data = population_data[
            (population_data["Time"] == 2020) & (population_data["Variant"] == "Medium")]
        reduced_popuation_data = reduced_popuation_data.groupby("Location").sum()
        reduced_popuation_data.rename(index={"Czechia": "Czech Republic"},
                                      inplace=True)

        best_population_data = reduced_popuation_data.loc[reduced_popuation_data.index.isin(countries_of_best)]
        best_population_data.loc[:, "PopTotal"] = pd.Series(best_population_data.loc[:, "PopTotal"] * 1000, dtype=int)
        best_population_data.to_csv(target_filepath)

        return best_population_data


def load_infection_data(infections_url, countries_of_best):

    infection_data = pd.read_csv(infections_url)
    infection_data.drop(columns=["Lat", "Long"], inplace=True)
    grouped_infection_data = infection_data.groupby("Country/Region").sum()
    grouped_infection_data.rename({"Moldova": "Republic of Moldova",
                                   "Russia": "Russian Federation",
                                   "Czechia": "Czech Republic"},
                                  inplace=True)
    best_infection_data = grouped_infection_data.loc[grouped_infection_data.index.isin(countries_of_best)]

    sorted_infection_dates = sorted([change_date_format_to_dmy(date) for date in best_infection_data.columns],
                                    key=itemgetter(6, 7, 3, 4, 0, 1))
    best_infection_data.columns = sorted_infection_dates

    return best_infection_data


def load_recovery_data(recoveries_url, countries_of_best):

    recovery_data = pd.read_csv(recoveries_url)
    recovery_data.drop(columns=["Lat", "Long"], inplace=True)
    grouped_recovery_data = recovery_data.groupby("Country/Region").sum()
    grouped_recovery_data.rename({"Moldova": "Republic of Moldova",
                                  "Russia": "Russian Federation",
                                  "Czechia": "Czech Republic"},
                                 inplace=True)
    best_recovery_data = grouped_recovery_data.loc[grouped_recovery_data.index.isin(countries_of_best)]

    sorted_recovery_dates = sorted([change_date_format_to_dmy(date) for date in best_recovery_data.columns],
                                   key=itemgetter(6, 7, 3, 4, 0, 1))

    best_recovery_data.columns = sorted_recovery_dates

    return best_recovery_data


def load_vaccination_data(vaccinations_url, countries_of_best):

    vaccination_data = pd.read_csv(vaccinations_url)
    vaccination_data.loc[vaccination_data.loc[:, "Country_Region"] == "Czechia", "Country_Region"] = 'Czech Republic'
    vaccination_data.loc[
        vaccination_data.loc[:, "Country_Region"] == "Moldova", "Country_Region"] = 'Republic of Moldova'
    vaccination_data.loc[vaccination_data.loc[:, "Country_Region"] == "Russia", "Country_Region"] = 'Russian Federation'

    reduced_vaccination_data = vaccination_data.loc[vaccination_data.loc[:, "Country_Region"].isin(countries_of_best)]
    reduced_vaccination_data = reduced_vaccination_data.groupby(["Country_Region", "Date"]).sum()

    partial_vaccination_data_frames = []
    full_vaccination_data_frames = []

    for country in countries_of_best:
        country_data = reduced_vaccination_data.loc[reduced_vaccination_data.index.get_level_values(0) == country]

        country_dates = [format_date_string(date) for date in country_data.index.get_level_values(1)]

        partial_vaccinations = country_data.loc[:, "People_partially_vaccinated"].to_numpy()
        full_vaccinations = country_data.loc[:, "People_fully_vaccinated"].to_numpy()

        country_name = (("Country/Region", pd.Series([country])),)
        partial_vaccination_data = tuple((date_string, pd.Series([partial_doses])) for date_string, partial_doses in
                                         zip(country_dates, partial_vaccinations))
        full_vaccination_data = tuple(
            (date_string, pd.Series([full_doses])) for date_string, full_doses in zip(country_dates, full_vaccinations))

        partial_vaccinations = OrderedDict(country_name + partial_vaccination_data)
        country_partial_vaccinations = pd.DataFrame(partial_vaccinations)
        partial_vaccination_data_frames.append(country_partial_vaccinations)

        full_vaccinations = OrderedDict(country_name + full_vaccination_data)
        country_full_vaccinations = pd.DataFrame(full_vaccinations)
        full_vaccination_data_frames.append(country_full_vaccinations)

    best_partial_vaccination_data = pd.concat(partial_vaccination_data_frames, ignore_index=True)
    best_full_vaccination_data = pd.concat(full_vaccination_data_frames, ignore_index=True)
    sorted_dates = sorted(best_partial_vaccination_data.columns, key=itemgetter(6, 7, 3, 4, 0, 1))

    best_partial_vaccination_data = best_partial_vaccination_data.loc[:, sorted_dates]
    best_partial_vaccination_data = best_partial_vaccination_data.groupby("Country/Region").sum()
    best_partial_vaccination_data = best_partial_vaccination_data.astype(int)

    best_full_vaccination_data = best_full_vaccination_data.loc[:, sorted_dates]
    best_full_vaccination_data = best_full_vaccination_data.groupby("Country/Region").sum()
    best_full_vaccination_data = best_full_vaccination_data.astype(int)

    return best_partial_vaccination_data, best_full_vaccination_data