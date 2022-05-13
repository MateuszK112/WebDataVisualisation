import dash
from dash import dcc, html, dash_table
import numpy as np
import plotly.graph_objects as pgo
from dash.dependencies import Input, Output
import os
import dash_bootstrap_components as dbc
import sqlite3
from project_app import *
from project_db import *

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 200)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.title = "Feet pressure data visualization"

server = app.server

app_color = {"graph_bg": "#000560", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        # header

        html.Div(
            [
                html.H1("Walking data visualization", className="app-header-title"),
                html.H3("Anomalies", className='anomaly')
            ], className='header'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [  # Feet pressure
                        html.Div(className='graph-title-div',
                                 children=[html.H2("Feet pressure over time graph", className="graph-title")]
                                 ),
                        dcc.Graph(
                            id='feet-pressure',
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    style_header={'color': '#0ce4bc', 'backgroundColor': '#000560',
                                                  'fontWeight': 'bold'},
                                    paper_bgcolor=app_color["graph_bg"],

                                )
                            )
                        ),
                        dcc.Interval(
                            id="feet-pressure-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                    ], className='main-chart', width=12
                ),
                dbc.Col(
                    [
                        dash_table.DataTable(

                            id="data-table",
                            columns=[{'name': 'patient_id', 'id': 'patient_id'},
                                     {'name': 'L1', 'id': 'L1'},
                                     {'name': 'L2', 'id': 'L2'},
                                     {'name': 'L3', 'id': 'L3'},
                                     {'name': 'R1', 'id': 'R1'},
                                     {'name': 'R2', 'id': 'R2'},
                                     {'name': 'R3', 'id': 'R3'}],
                            data=[{'patient_id': '1', "L1": '--', "L2": '--', "L3": '--', "R1": '--', "R2": '--',
                                   "R3": '--'}],
                            editable=True,
                            page_action='none',
                            style_data={'color': '#0ce4bc', 'backgroundColor': '#000560'},
                            style_header={'color': '#0ce4bc', 'backgroundColor': '#000560', 'fontWeight': 'bold'},
                            style_table={'height': '510px', 'overflowY': 'auto'}),

                        dcc.Interval(
                            id="data-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),

                    ]
                )

            ], className='main-content'

        ),
        dbc.Row(
            [  # buttons
                dbc.Col(
                    [
                        dcc.RadioItems(
                            id='patients',
                            options=[
                                {'label': 'Patient 1', 'value': 10},
                                {'label': 'Patient 2', 'value': 20},
                                {'label': 'Patient 3', 'value': 30},
                                {'label': 'Patient 4', 'value': 40},
                                {'label': 'Patient 5', 'value': 50},
                                {'label': 'Patient 6', 'value': 60},

                            ],
                            value=10,
                            className='values-checklist'
                        )
                    ], width=3
                ),
                dbc.Col(
                    [
                        dcc.Checklist(
                            id='parts',
                            options=[
                                {'label': 'L1 ', 'value': 1},
                                {'label': 'L2 ', 'value': 2},
                                {'label': 'L3 ', 'value': 3},
                                {'label': 'R1 ', 'value': 4},
                                {'label': 'R2 ', 'value': 5},
                                {'label': 'R3 ', 'value': 6}
                            ],
                            value=[1, 2],
                            labelStyle={'display': 'inline-block'},
                            className='values-checklist'
                        )
                    ], width=3
                ),

                dbc.Col(
                    [
                        html.Div([
                            dcc.Slider(
                                id='my-slider',
                                min=0.5,
                                max=10,
                                step=0.5,
                                value=0.5,
                                marks={
                                    0.5: 'current time',
                                    5: '5 minutes ago',
                                    10: '10 minutes ago'
                                },
                            )
                        ])

                    ]
                )

            ], className='buttons'
        ),

    ]
)


@app.callback(
    Output("data-table", "data"), Input("data-update", "n_intervals"), Input("patients", "value")
)
def update_tab(n_intervals, value):
    ctx = dash.callback_context

    db_upd_tab = get_anomaly_data()  # cursor.fetchall()

    anomaly_data = []
    for i in db_upd_tab:
        anomaly = {"patient_id": i[0], "L1": i[1], "L2": i[2], "L3": i[3], "R1": i[4], "R2": i[5], "R3": i[6]}
        anomaly_data.append(anomaly)

    return anomaly_data


@app.callback(
    Output("feet-pressure", "figure"), Input("feet-pressure-update", "n_intervals"), Input("parts", "value"),
    Input("patients", "value"), Input("my-slider", "value")
)
def feet_pressure_data(n_intervals, value, value_patient, slider_value):
    ctx = dash.callback_context

    feet_pressure_db = get_all_data()

    recent_tstamp = []
    oldest_tstamp = []
    tstamp_border = [0]

    temp_pid = [i[14] for i in feet_pressure_db if i[1] == '1']
    temp_pid.sort(reverse=True)
    recent_tstamp.append(temp_pid[0])
    oldest_tstamp.append(temp_pid[-1])

    if recent_tstamp[0] - oldest_tstamp[0] < (list(ctx.inputs.values())[3] * 60):
        tstamp_border[0] = oldest_tstamp[0]
    else:
        tstamp_border[0] = recent_tstamp[0] - (list(ctx.inputs.values())[3] * 60)

    x = [i[0] for i in feet_pressure_db if i[1] == '1']
    y = [i[2] for i in feet_pressure_db if i[1] == '1']

    fig1 = pgo.Figure(
        pgo.Scatter(x=np.array(x), y=np.array(y),
                    marker={'color': 'red'}, visible=False))

    patient_list = [10, 20, 30, 40, 50, 60]

    for value in patient_list:

        if list(ctx.inputs.values())[2] == value:
            patient = str(int(value / 10))

            x = [i[0] for i in feet_pressure_db if
                 i[1] == patient and tstamp_border[0] < i[14] < tstamp_border[0] + 30]
            y = [i[2] for i in feet_pressure_db if
                 i[1] == patient and tstamp_border[0] < i[14] < tstamp_border[0] + 30]
            fig1 = pgo.Figure(
                pgo.Scatter(x=(np.array(x)),
                            y=(np.array(y)),
                            marker={'color': 'red'},
                            visible=False,
                            mode='lines+markers'))

            fig1['layout']['xaxis']['title'] = 'timestamps'
            fig1['layout']['yaxis']['title'] = 'pressure values'

            color_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
            traces_list = [1, 2, 3, 4, 5, 6]
            names_list = ["L1", "L2", "L3", "R1", "R2", "R3"]
            for trace, color, name in zip(traces_list, color_list, names_list):
                if trace in list(ctx.inputs.values())[1]:
                    x = [i[0] for i in feet_pressure_db if
                         i[1] == patient and tstamp_border[0] < i[14] < tstamp_border[0] + 30]
                    y = [i[1 + trace] for i in feet_pressure_db if
                         i[1] == patient and tstamp_border[0] < i[14] < tstamp_border[0] + 30]
                    fig1.add_trace(
                        pgo.Scatter(x=(np.array(x)),
                                    y=(np.array(y)),
                                    marker={'color': color},
                                    name=name,
                                    visible=True,
                                    mode='lines+markers'))

                    x = [i[0] for i in feet_pressure_db if
                         i[1] == patient and i[7 + trace] == '1' and tstamp_border[0] < i[14] <
                         tstamp_border[0] + 30]
                    y = [i[1 + trace] for i in feet_pressure_db if
                         i[1] == patient and i[7 + trace] == '1' and tstamp_border[0] < i[14] <
                         tstamp_border[0] + 30]
                    fig1.add_trace(pgo.Scatter(x=(np.array(x)),
                                               y=(np.array(y)),
                                               marker={'color': color}, line=dict(width=0), visible=True,
                                               marker_size=16,
                                               showlegend=False,
                                               mode='lines+markers'))

            return fig1

    return fig1


if __name__ == "__main__":

    make_database()
    time_check = tm.time()

    delete_data()

    data_thr = Get_Data()
    data_thr.start()
    try:
        app.run_server()
    finally:
        stop_getting_data = True
        data_thr.join()
        print("Getting data has successfully ended!")
