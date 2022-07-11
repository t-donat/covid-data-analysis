from covid_dashboard import create_app

if __name__ == "__main__":

    dashboard_app = create_app()

    dashboard_app.run_server(debug=False)
    # dashboard_app.run_server(debug=True)
