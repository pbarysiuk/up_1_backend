from urllib.parse import unquote
from src.threeDimPlot.synergy import Synergy
from json import loads

def lambda_handler(event, context):
    action = event['pathParameters']['proxy']
    E0 = event['queryStringParameters'].get('E0')
    if E0 is not None:
        E0 = float(E0)
    alpha12_slider_value = event['queryStringParameters'].get('alpha12_slider_value')
    if alpha12_slider_value is not None:
        alpha12_slider_value = float(alpha12_slider_value)
    alpha21_slider_value = event['queryStringParameters'].get('alpha21_slider_value')
    if alpha21_slider_value is not None:
        alpha21_slider_value = float(alpha21_slider_value)
    gamma12_slider_value = event['queryStringParameters'].get('gamma12_slider_value')
    if gamma12_slider_value is not None:
        gamma12_slider_value = float(gamma12_slider_value)
    gamma21_slider_value = event['queryStringParameters'].get('gamma21_slider_value')
    if gamma21_slider_value is not None:
        gamma21_slider_value = float(gamma21_slider_value)
    beta_slider_value = event['queryStringParameters'].get('beta_slider_value')
    if beta_slider_value is not None:
        beta_slider_value = float(beta_slider_value)
    E1_slider_value = event['queryStringParameters'].get('E1_slider_value')
    if E1_slider_value is not None:
        E1_slider_value = float(E1_slider_value)
    E2_slider_value = event['queryStringParameters'].get('E2_slider_value')
    if E2_slider_value is not None:
        E2_slider_value = float(E2_slider_value)
    C1_slider_value = event['queryStringParameters'].get('C1_slider_value')
    if C1_slider_value is not None:
        C1_slider_value = float(C1_slider_value)
    C2_slider_value = event['queryStringParameters'].get('C2_slider_value')
    if C2_slider_value is not None:
        C2_slider_value = float(C2_slider_value)
    h1_slider_value = event['queryStringParameters'].get('h1_slider_value')
    if h1_slider_value is not None:
        h1_slider_value = float(h1_slider_value)
    h2_slider_value = event['queryStringParameters'].get('h2_slider_value')
    if h2_slider_value is not None:
        h2_slider_value = float(h2_slider_value) 
    return Synergy.calculatePlot(action=action, E0=E0, alpha12_slider_value=alpha12_slider_value,  alpha21_slider_value=alpha21_slider_value, gamma12_slider_value=gamma12_slider_value,  gamma21_slider_value=gamma21_slider_value, beta_slider_value=beta_slider_value,  E1_slider_value=E1_slider_value,  E2_slider_value=E2_slider_value, C1_slider_value=C1_slider_value,  C2_slider_value=C2_slider_value,h1_slider_value=h1_slider_value, h2_slider_value=h2_slider_value)
