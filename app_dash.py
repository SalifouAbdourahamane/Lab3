# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash import Dash, dcc, html, Input, Output, State
from dash import Dash, dash_table
import plotly.express as px
import pandas as pd
import requests

# API configuration
API_BASE_URL = "http://localhost:4000"

# Initialize app
app = Dash(__name__)
df = pd.read_csv("iris_extended_encoded.csv", sep=',')
df_csv = df.to_csv(index=False)

# Styles
tabs_styles = {'height': '44px'}
tab_style = {'borderBottom': '1px solid #d6d6d6', 'padding': '6px', 'fontWeight': 'bold'}
tab_selected_style = {'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6',
                     'backgroundColor': '#119DFF', 'color': 'white', 'padding': '6px'}
col_style = {'display':'grid', 'grid-auto-flow': 'row'}
row_style = {'display':'grid', 'grid-auto-flow': 'column'}

app.layout = html.Div(children=[
    html.H1(children='Iris classifier'),
    dcc.Tabs([
    dcc.Tab(label="Explore Iris training data", style=tab_style, selected_style=tab_selected_style, children=[
        html.Div([
            html.Div([
                html.Label(['File name to Load for training or testing'], style={'font-weight': 'bold'}),
                dcc.Input(id='file-for-train', type='text', style={'width':'100px'}),
                html.Div([
                    html.Button('Load', id='load-val', style={"width":"60px", "height":"30px"}),
                    html.Div(id='load-response', children='Click to load')
                ], style=col_style)
            ], style=col_style),
            html.Div([
                html.Button('Upload', id='upload-val', style={"width":"60px", "height":"30px"}),
                html.Div(id='upload-response', children='Click to upload')
            ], style=col_style| {'margin-top':'20px'})
        ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),
        html.Div([
            html.Div([
                html.Div([
                    html.Label(['Feature'], style={'font-weight': 'bold'}),
                    dcc.Dropdown(df.columns[1:].tolist(), df.columns[1], id='hist-column')
                ], style=col_style),
                dcc.Graph(id='selected_hist')
            ], style=col_style | {'height':'400px', 'width':'400px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label(['X-Axis'], style={'font-weight': 'bold'}),
                        dcc.Dropdown(df.columns[1:].tolist(), df.columns[1], id='xaxis-column')
                    ]),
                    html.Div([
                        html.Label(['Y-Axis'], style={'font-weight': 'bold'}),
                        dcc.Dropdown(df.columns[1:].tolist(), df.columns[2], id='yaxis-column')
                    ])
                ], style=row_style | {'margin-left':'50px', 'margin-right': '50px'}),
                dcc.Graph(id='indicator-graphic')
            ], style=col_style)
        ], style=row_style),
        html.Div(id='tablecontainer', children=[
            dash_table.DataTable(df.to_dict('records'), 
            [{"name": i, "id": i} for i in df.columns], page_size=15, id='datatable')
        ])
    ]),
    dcc.Tab(label="Build model and perform training", id="train-tab", style=tab_style, selected_style=tab_selected_style, children=[
        html.Div([
            html.Div([
                html.Label(['Enter a dataset ID to use in training'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='dataset-for-train', type='text'))
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Button('New model', id='build-val', style={'width':'90px', "height":"30px"}),
                html.Div(id='build-response', children='Click to build new model and train')
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Label(['Enter a model ID for re-training'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='model-for-train', type='text'))
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Button('Re-Train', id='train-val', style={"width":"90px", "height":"30px"})
            ], style=col_style | {'margin-top':'20px', 'width':'90px'})
        ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),
        html.Div(id='container-button-train', children='')
    ]),
    dcc.Tab(label="Score model", id="score-tab", style=tab_style, selected_style=tab_selected_style, children=[
        html.Div([
            html.Div([
                html.Label(['Enter a row text (CSV) to use in scoring'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='row-for-score', type='text', style={'width':'300px'}))
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Label(['Enter a model ID for scoring'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='model-for-score', type='text'))
            ], style=col_style | {'margin-top':'20px'}),            
            html.Div([
                html.Button('Score', id='score-val', style={'width':'90px', "height":"30px"}),
                html.Div(id='score-response', children='Click to score')
            ], style=col_style | {'margin-top':'20px'})
        ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),
        html.Div(id='container-button-score', children='')
    ]),
    dcc.Tab(label="Test Iris data", style=tab_style, selected_style=tab_selected_style, children=[
        html.Div([
            html.Div([
                html.Label(['Enter a dataset ID to use in testing'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='dataset-for-test', type='text'))
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Label(['Enter a model ID to use in testing'], style={'font-weight': 'bold'}),
                html.Div(dcc.Input(id='model-for-test', type='text'))
            ], style=col_style | {'margin-top':'20px'}),
            html.Div([
                html.Button('Test', id='test-val'),
            ], style=col_style | {'margin-top':'20px', 'width':'90px'})
        ], style=col_style | {'margin-top':'50px', 'margin-bottom':'50px', 'width':"400px", 'border': '2px solid black'}),
        html.Div(id='container-button-test', children='')
    ])
    ])
])

from dash import callback_context, no_update
import dash

# Callbacks for Explore Data tab
@app.callback(
    [Output('load-response', 'children'),
     Output('upload-response', 'children'),
     Output('datatable', 'data')],
    [Input('load-val', 'n_clicks'),
     Input('upload-val', 'n_clicks')],
    [State('file-for-train', 'value')],
    prevent_initial_call=True
)
def handle_data_actions(load_clicks, upload_clicks, filename):
    ctx = callback_context
    if not ctx.triggered:
        return no_update, no_update, no_update
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    global df, df_csv
    
    if triggered_id == 'load-val' and load_clicks and filename:
        try:
            df = pd.read_csv(filename)
            df_csv = df.to_csv(index=False)
            return f'Loaded {filename} successfully', no_update, df.to_dict('records')
        except Exception as e:
            return f'Error loading file: {str(e)}', no_update, no_update
    
    elif triggered_id == 'upload-val' and upload_clicks and filename:
        try:
            with open(filename, 'rb') as f:
                response = requests.post(
                    f"{API_BASE_URL}/iris/datasets", 
                    files={'file': f},
                    timeout=10
                )
            if response.status_code == 201:
                return no_update, f'Dataset ID: {response.json()["dataset_id"]}', no_update
            return no_update, f'Upload failed: {response.text}', no_update
        except Exception as e:
            return no_update, f'Error: {str(e)}', no_update
    
    return no_update, no_update, no_update

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('load-val', 'n_clicks')]
)
def update_graph(xaxis_column_name, yaxis_column_name, _):
    fig = px.scatter(
        df, 
        x=xaxis_column_name, 
        y=yaxis_column_name,
        title=f"{yaxis_column_name} vs {xaxis_column_name}"
    )
    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, 
        hovermode='closest'
    )
    return fig

@app.callback(
    Output('selected_hist', 'figure'),
    [Input('hist-column', 'value'),
     Input('load-val', 'n_clicks')]
)
def update_hist(hist_column_name, _):
    fig = px.histogram(
        df, 
        x=hist_column_name,
        title=f"Distribution of {hist_column_name}"
    )
    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, 
        hovermode='closest'
    )
    return fig

# Training Tab Callbacks
@app.callback(
    [Output('build-response', 'children'),
     Output('container-button-train', 'children')],
    [Input('build-val', 'n_clicks'),
     Input('train-val', 'n_clicks')],
    [State('dataset-for-train', 'value'),
     State('model-for-train', 'value')],
    prevent_initial_call=True
)
def handle_training_actions(build_clicks, train_clicks, dataset_id, model_id):
    ctx = callback_context
    if not ctx.triggered:
        return no_update, no_update
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'build-val' and build_clicks:
        try:
            dataset_id = int(dataset_id) if dataset_id else 0
            response = requests.post(
                f"{API_BASE_URL}/iris/model/new",
                data={'dataset': dataset_id},
                timeout=10
            )
            if response.status_code == 201:
                result = response.json()
                return f"Model ID: {result['model_id']} created", no_update
            return f"API Error: {response.text}", no_update
        except Exception as e:
            return f"Error: {str(e)}", no_update
    
    elif triggered_id == 'train-val' and train_clicks:
        try:
            model_id = int(model_id) if model_id else 0
            dataset_id = int(dataset_id) if dataset_id else 0
            
            response = requests.put(
                f"{API_BASE_URL}/iris/model/{model_id}/train?dataset={dataset_id}",
                timeout=15
            )
            
            if response.status_code == 200:
                history = response.json()
                epochs = range(1, len(history['loss']) + 1)
                
                train_df = pd.DataFrame({
                    'Epoch': epochs,
                    'Loss': history['loss'],
                    'Accuracy': history['accuracy']
                })
                
                fig = px.line(
                    train_df,
                    x='Epoch',
                    y=['Loss', 'Accuracy'],
                    title='Training Metrics',
                    labels={'value': 'Metric Value', 'variable': 'Metric'}
                )
                fig.update_traces(line=dict(width=2.5))
                fig.update_layout(hovermode='x unified')
                
                return no_update, dcc.Graph(figure=fig)
            return no_update, f"API Error: {response.text}"
        except Exception as e:
            return no_update, f"Error: {str(e)}"
    
    return no_update, no_update

# Scoring Tab Callback
@app.callback(
    Output('container-button-score', 'children'),
    Input('score-val', 'n_clicks'),
    [State('model-for-score', 'value'),
     State('row-for-score', 'value')],
    prevent_initial_call=True
)
def update_output_score(n_clicks, model_id, row):
    if n_clicks and model_id and row:
        try:
            features = list(map(float, row.split(',')))
            if len(features) != 20:
                return "Error: Exactly 20 features required"
                
            response = requests.post(
                f"{API_BASE_URL}/iris/model/{model_id}/predict",
                json={'features': features},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                probabilities = [f"{p:.4f}" for p in result['probabilities']]
                
                return html.Div([
                    html.H4(f"Predicted species: {result['species']}", 
                            style={'color': '#119DFF', 'margin-bottom': '10px'}),
                    html.P("Class probabilities:", style={'font-weight': 'bold'}),
                    html.Ul([
                        html.Li(f"Setosa: {probabilities[0]}"),
                        html.Li(f"Versicolor: {probabilities[1]}"),
                        html.Li(f"Virginica: {probabilities[2]}")
                    ])
                ], style={'margin-top': '20px'})
            return f'API Error: {response.text}'
        except ValueError:
            return "Error: All values must be numbers"
        except Exception as e:
            return f'Error: {str(e)}'
    return no_update

# Testing Tab Callback
@app.callback(
    Output('container-button-test', 'children'),
    Input('test-val', 'n_clicks'),
    [State('model-for-test', 'value'),
     State('dataset-for-test', 'value')],
    prevent_initial_call=True
)
def update_output_test(n_clicks, model_id, dataset_id):
    if n_clicks and model_id and dataset_id:
        try:
            response = requests.get(
                f"{API_BASE_URL}/iris/model/{model_id}/test?dataset={dataset_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                test_df = pd.DataFrame({
                    'Metric': ['Accuracy', 'Loss'],
                    'Value': [results['accuracy'], results['loss']]
                })
                
                fig = px.bar(
                    test_df,
                    x='Metric',
                    y='Value',
                    title='Model Test Results',
                    color='Metric',
                    text_auto='.2f'
                )
                fig.update_layout(
                    yaxis_range=[0, 1],
                    showlegend=False
                )
                
                return html.Div([
                    dcc.Graph(figure=fig),
                    html.P(f"Actual vs Predicted match: {sum(a == p for a, p in zip(results['actual'], results['predicted']))}/{len(results['actual'])}")
                ])
            return f'API Error: {response.text}'
        except Exception as e:
            return f'Error: {str(e)}'
    return no_update
if __name__ == '__main__':
    app.run(debug=True)