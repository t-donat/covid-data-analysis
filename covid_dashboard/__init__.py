import pandas as pd
import json
import configparser
import os

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from covid_dashboard.data import load_population_data, load_vaccination_data, load_recovery_data, load_infection_data
from covid_dashboard.layouts import create_home_layout, create_about_layout
from covid_dashboard.layouts import create_infections_layout, create_vaccination_layout


def create_app():

    app = dash.Dash(__name__,
                    external_stylesheets=[dbc.themes.BOOTSTRAP])

    @callback(Output(component_id="page_content", component_property="children"),
              [Input(component_id="page_url", component_property="pathname")])
    def render_page(pathname):

        if pathname == "/":
            return create_home_layout()

        elif pathname == "/infections/":
            return create_infections_layout(country_names=supported_countries)

        elif pathname == "/vaccinations/":
            return create_vaccination_layout(country_names=supported_countries)

        elif pathname == "/about":
            return create_about_layout()

        else:
            return "<h1>Test</h1>"

    the_navbar = dbc.Navbar(
        dbc.Container([
            html.A(dbc.Row([
                # dbc.Col(html.Img(src=PAGE_LOGO, height="30px")),
                dbc.Col(dbc.NavbarBrand("Covid Dashboard", className="ms-2"))
            ],
             align="center0",
             className="g-0"),
                   href="/",
                   style={"textDecoration": "none"}),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Infections", href="/infections/")),
                dbc.NavItem(dbc.NavLink("Vaccinations", href="/vaccinations/")),
                dbc.NavItem(dbc.NavLink("About", href="/about")),
            ])
        ]),
        color="dark",
        dark=True

    )

    # the_navbar = html.Div([
    #            dcc.Location(id="navbar_id"),

    #            html.Div(dcc.Link("Home", href="/"), className="nav_bar_box"),
    #            html.Div(dcc.Link("Infections", href="/infections/"), className="nav_bar_box"),
    #            html.Div(dcc.Link("Vaccinations", href="/vaccinations/"), className="nav_bar_box"),
    #            html.Div(dcc.Link("About", href="/about"), className="nav_bar_box"),

    #        ], id="page_navbar")

    the_top = html.Div([
                dcc.Location(id="page_url", refresh=False),
                the_navbar
    ],
     id="top_bar_content",
     className="content_box")

    page_content = html.Div(id="page_content",
                            className="content_box")

    app.layout = html.Div([the_top,
                           page_content],
                          style={"height": "90vh",
                                 "width": "100vw"})

    # HOME PAGE

    config_directory = os.path.join(os.path.dirname(__file__),
                                    "config")

    config = configparser.ConfigParser()
    config.read(os.path.join(config_directory, "dashboard.cfg"))

    population_url = config["population"]["data_url"]
    infections_url = config["infections"]["data_url"]
    recoveries_url = config["recoveries"]["data_url"]
    vaccinations_url = config["vaccinations"]["data_url"]

    with open(os.path.join(config_directory, "countries_of_best.json"), "r") as country_file:
        contents = json.load(country_file)

    supported_countries = contents["countries"]

    population_data = load_population_data(population_url, supported_countries)
    infection_data = load_infection_data(infections_url, supported_countries)
    recovery_data = load_recovery_data(recoveries_url, supported_countries)
    partial_vaccination_data, full_vaccination_data = load_vaccination_data(vaccinations_url, supported_countries)

    # infections
    daily_infections = infection_data.diff(axis=1).fillna(value=0)

    three_day_avg_infections = daily_infections.iloc[:, -3:].mean(axis=1)
    seven_day_avg_infections = daily_infections.iloc[:, -7:].mean(axis=1)
    fourteen_day_avg_infections = daily_infections.iloc[:, -14:].mean(axis=1)

    # incidence
    three_day_incidence = daily_infections.iloc[:, -3:].sum(axis=1) * 100_000 / population_data.loc[:, "PopTotal"]
    seven_day_incidence = daily_infections.iloc[:, -7:].sum(axis=1) * 100_000 / population_data.loc[:, "PopTotal"]
    fourteen_day_incidence = daily_infections.iloc[:, -14:].sum(axis=1) * 100_000 / population_data.loc[:, "PopTotal"]

    # vaccinations
    partial_vaccination_percentage = partial_vaccination_data.iloc[:, -1] * 100 / population_data.loc[:, "PopTotal"]
    full_vaccination_percentage = full_vaccination_data.iloc[:, -1] * 100 / population_data.loc[:, "PopTotal"]

    # bring it all together
    quick_info = pd.DataFrame({"three_day_avg_infections": three_day_avg_infections,
                               "seven_day_avg_infections": seven_day_avg_infections,
                               "fourteen_day_avg_infections": fourteen_day_avg_infections,
                               "three_day_incidence": three_day_incidence,
                               "seven_day_incidence": seven_day_incidence,
                               "fourteen_day_incidence": fourteen_day_incidence,
                               "partial_vaccination_percentage": partial_vaccination_percentage,
                               "full_vaccination_percentage": full_vaccination_percentage})

    quick_info = quick_info.round(2)

    with open("./covid_dashboard/config/map.geojson", "r") as geo_data:
        map_geometry = json.load(geo_data)

    @callback(Output(component_id="graph_title", component_property="children"),
              Input(component_id="graph_selector", component_property="value"))
    def render_home_title(display_mode):

        if display_mode == "fully_vaccinated":
            graph_title = "Full Vaccinations"

        elif display_mode == "partially_vaccinated":
            graph_title = "Partial Vaccinations"

        elif display_mode == "three_day_avg":
            graph_title = "Three day average of daily infections"

        elif display_mode == "seven_day_avg":
            graph_title = "Seven day average of daily infections"

        elif display_mode == "fourteen_day_avg":
            graph_title = "Fourteen day average of daily infections"

        elif display_mode == "three_day_incidence":
            graph_title = "Incidence over the last 3 days per 100 000"

        elif display_mode == "seven_day_incidence":
            graph_title = "Incidence over the last 7 days per 100 000"

        elif display_mode == "fourteen_day_incidence":
            graph_title = "Incidence over the last 14 days per 100 000"

        else:
            raise ValueError(f"Unknown display mode: '{display_mode}'")

        return graph_title

    @callback(Output(component_id="map_graph", component_property="figure"),
              Input(component_id="graph_selector", component_property="value"))
    def render_home_graph(display_mode):
        # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        if display_mode == "fully_vaccinated":
            values_for_graph = quick_info["full_vaccination_percentage"]
            hover_template_extra_text = "<b>%{z}%</b> of population fully vaccinated"

        elif display_mode == "partially_vaccinated":
            values_for_graph = quick_info["partial_vaccination_percentage"]
            hover_template_extra_text = "<b>%{z}%</b> of population partially vaccinated"

        elif display_mode == "three_day_avg":
            values_for_graph = quick_info["three_day_avg_infections"]
            hover_template_extra_text = "On average <b>%{z}</b> new cases over the last <b>3 days</b>"

        elif display_mode == "seven_day_avg":
            values_for_graph = quick_info["seven_day_avg_infections"]
            hover_template_extra_text = "On average <b>%{z}</b> new cases over the last <b>7 days</b>"

        elif display_mode == "fourteen_day_avg":
            values_for_graph = quick_info["fourteen_day_avg_infections"]
            hover_template_extra_text = "On average <b>%{z}</b> new cases over the last <b>14 days</b>"

        elif display_mode == "three_day_incidence":
            values_for_graph = quick_info["three_day_incidence"]
            hover_template_extra_text = "<b>%{z}</b> new cases over the last <b>3 days</b>"

        elif display_mode == "seven_day_incidence":
            values_for_graph = quick_info["seven_day_incidence"]
            hover_template_extra_text = "<b>%{z}</b> new cases over the last <b>7 days</b>"

        elif display_mode == "fourteen_day_incidence":
            values_for_graph = quick_info["fourteen_day_incidence"]
            hover_template_extra_text = "<b>%{z}</b> new cases over the last <b>14 days</b>"

        else:
            raise ValueError(f"Unknown display mode: '{display_mode}'")

        fig = go.Figure()

        map_trace = go.Choroplethmapbox(geojson=map_geometry,
                                        locations=quick_info.index,
                                        featureidkey="properties.name_long",
                                        z=values_for_graph,
                                        colorscale="blues",
                                        marker_opacity=0.6,
                                        hovertemplate="<b>%{location}</b><br>" +
                                                      f"<extra>{hover_template_extra_text}</extra>")

        fig.add_trace(map_trace)

        fig.update_layout(title={"text": "Test 123"},
                          mapbox_style="carto-positron",
                          mapbox_zoom=2.9,
                          mapbox_center={"lat": 57.20756956834978,
                                         "lon": 11.988806419969213},
                          margin={"r": 0,
                                  "t": 0,
                                  "l": 0,
                                  "b": 0})

        fig.update_geos(
            fitbounds="locations",
            resolution=50,
            visible=False,
            showframe=False,
            projection={"type": "mercator"},
        )

        return fig

    # INFECTIONS PAGE

    @callback(Output(component_id="infections_graph", component_property="figure"),
              [Input(component_id="country_selection", component_property="value"),
               Input(component_id="mode_selection", component_property="value")])
    def render_infections_graph(selected_countries, display_mode):
        fig = go.Figure()

        if not isinstance(selected_countries, (str, list)):
            TypeError("Parameter 'selected_countries' is of unsupported type")

        if isinstance(selected_countries, str):
            selected_countries = [selected_countries]

        x_axis_dates = infection_data.columns

        for current_country in selected_countries:

            if display_mode == "total":
                country_data = infection_data.loc[current_country]

            else:
                country_data = infection_data.loc[current_country].diff()

                if display_mode == "3_day_average":
                    country_data = country_data.rolling(window=3).mean()

                if display_mode == "7_day_average":
                    country_data = country_data.rolling(window=7).mean()

                if display_mode == "14_day_average":
                    country_data = country_data.rolling(window=14).mean()

            country_data = country_data.fillna(value=0.0)

            country_plot = go.Scatter(x=x_axis_dates,
                                      y=country_data,
                                      mode="lines",
                                      name=current_country)

            fig.add_trace(country_plot)

        # fig.update_layout(xaxis={"tickformat": "%a %B %Y"})
        fig.update_layout(xaxis={"tickmode": "auto",
                                 "nticks": 10})

        return fig

        # INFECTIONS PAGE

    @callback(Output(component_id="vaccine_graph", component_property="figure"),
              [Input(component_id="country_selection", component_property="value"),
               Input(component_id="mode_selection", component_property="value")])
    def render_vaccine_graph(selected_countries, display_mode):
        fig = go.Figure()

        if not isinstance(selected_countries, (str, list)):
            TypeError("Parameter 'selected_countries' is of unsupported type")

        if isinstance(selected_countries, str):
            selected_countries = [selected_countries]

        x_axis_dates = full_vaccination_data.columns

        for current_country in selected_countries:

            if "full" in display_mode:
                country_data = full_vaccination_data.loc[current_country]

            elif "partial" in display_mode:
                country_data = partial_vaccination_data.loc[current_country]

            else:
                raise ValueError(f"Unknown display mode '{display_mode}'")

            if "percentage" in display_mode:
                country_data = 100 * country_data / population_data.loc[current_country, "PopTotal"]

            country_data = country_data.fillna(value=0.0)

            country_plot = go.Scatter(x=x_axis_dates,
                                      y=country_data,
                                      mode="lines",
                                      name=current_country)

            fig.add_trace(country_plot)

        # fig.update_layout(xaxis={"tickformat": "%a %B %Y"})
        fig.update_layout(xaxis={"tickmode": "auto",
                                 "nticks": 10})

        if "percentage" in display_mode:
            fig.update_layout(yaxis={"range": [0, 100],
                                     "title": "% of population"})

        return fig

    return app
    # app.run_server(debug=True)


