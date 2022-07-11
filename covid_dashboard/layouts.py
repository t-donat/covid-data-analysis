import os
import configparser

from dash import html
from dash import dcc
import plotly.graph_objects as go


def create_home_layout():
    empty_map = go.Choroplethmapbox()
    empty_figure = go.Figure()

    empty_figure.add_trace(empty_map)
    empty_figure.update_layout(title={"text": "Test 123"},
                               mapbox_style="carto-positron",
                               mapbox_zoom=2.0,
                               mapbox_center={"lat": 57.20756956834978,
                                              "lon": 11.988806419969213},
                               margin={"r": 0,
                                       "t": 0,
                                       "l": 0,
                                       "b": 0})

    empty_figure.update_geos(
        fitbounds="locations",
        resolution=50,
        visible=False,
        showframe=False,
        projection={"type": "mercator"},
    )

    layout = [html.H2(id="graph_title"),
              dcc.Dropdown(options=[{"label": "Full Vaccinations", "value": "fully_vaccinated"},
                                    {"label": "Partial Vaccinations", "value": "partially_vaccinated"},
                                    {"label": "Incidence over the last 3 days per 100 000",
                                     "value": "three_day_incidence"},
                                    {"label": "Incidence over the last 7 days per 100 000",
                                     "value": "seven_day_incidence"},
                                    {"label": "Incidence over the last 14 days per 100 000",
                                     "value": "fourteen_day_incidence"},
                                    {"label": "Three day average of daily infections", "value": "three_day_avg"},
                                    {"label": "Seven day average of daily infections", "value": "seven_day_avg"},
                                    {"label": "Fourteen day average of daily infections", "value": "fourteen_day_avg"}],
                           value="fully_vaccinated",
                           id="graph_selector"),
              dcc.Graph(id="map_graph")]

    return layout


def create_infections_layout(country_names):

    layout = [html.H2("Infections", id="graph_title"),
              dcc.Dropdown(options=[{"label": country, "value": country} for country in country_names],
                           multi=True,
                           value="Austria",
                           placeholder="Select a country...",
                           id="country_selection"),
              dcc.Dropdown(options=[{"label": "Total number of infections", "value": "total"},
                                    {"label": "Daily infections", "value": "daily"},
                                    {"label": "3-day average of daily infections", "value": "3_day_average"},
                                    {"label": "7-day average of daily infections", "value": "7_day_average"},
                                    {"label": "14-day average of daily infections", "value": "14_day_average"}],
                           value="daily",
                           id="mode_selection"),
              dcc.Graph(id="infections_graph")]
    return layout


def create_vaccination_layout(country_names):

    layout = [html.H2("Vaccinations", id="graph_title"),
              dcc.Dropdown(options=[{"label": country, "value": country} for country in country_names],
                           multi=True,
                           value="Austria",
                           placeholder="Select a country...",
                           id="country_selection"),
              dcc.Dropdown(options=[{"label": "Partial Vaccinations", "value": "partial"},
                                    {"label": "Partial Vaccinations (% of population)", "value": "partial_percentage"},
                                    {"label": "Full Vaccinations", "value": "full"},
                                    {"label": "Full Vaccinations (% of population)", "value": "full_percentage"}],
                           value="full_percentage",
                           id="mode_selection"),
              dcc.Graph(id="vaccine_graph")]

    return layout


def create_about_layout():
    config_directory = os.path.join(os.path.dirname(__file__),
                                    "config")

    config = configparser.ConfigParser()
    config.read(os.path.join(config_directory, "dashboard.cfg"))

    layout = [
        html.H2("About"),
        html.P("""This is a hobby-made page for tracking data regarding the SARS‑CoV‑2 pandemic. 
            The data are taken from different sources stated below, I do not vouch for their correctness or the correctness
            of the derivative data calculated from the original sources (e.g. incidence over X days per 100 000 citizens).
            """),
        html.Br(),
        html.H3("Sources"),

        html.P(["Infection data: ",
                html.A(config["infections"]["source_institution"],
                       href=config["infections"]["source_url"])
                ]),

        html.P(["Vaccination data: ",
                html.A(config["vaccinations"]["source_institution"],
                       href=config["vaccinations"]["source_url"])
                ]),

        html.P(["Recovery data: ",
                html.A(config["recoveries"]["source_institution"],
                       href=config["recoveries"]["source_url"])
                ]),

        html.P(["Population data: ",
                html.A(config["population"]["source_institution"],
                       href=config["population"]["source_url"])
                ]),

        html.Br(),

        html.H3("Impressum"),
        html.P("Seitenbesitzer: Tobias Donat"),
        html.P("Adresse: Brennerstraße 23, 4040 Linz, Österreich"),
        html.P("Email: tobias.donat@gmx.at"),
    ]

    return layout
