from urllib.parse import unquote
from src.threeDimPlot.synergy import Synergy
from json import loads
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    action = LambdaHelper.getPathParam(event, 'proxy')
    E0 = LambdaHelper.getQueryStringParam(event, 'E0', LambdaHelper.valueTypeFloat)
    alpha12_slider_value = LambdaHelper.getQueryStringParam(event, 'alpha12_slider_value', LambdaHelper.valueTypeFloat)
    alpha21_slider_value = LambdaHelper.getQueryStringParam(event, 'alpha21_slider_value', LambdaHelper.valueTypeFloat)
    gamma12_slider_value = LambdaHelper.getQueryStringParam(event, 'gamma12_slider_value', LambdaHelper.valueTypeFloat)
    gamma21_slider_value = LambdaHelper.getQueryStringParam(event, 'gamma21_slider_value', LambdaHelper.valueTypeFloat)
    beta_slider_value = LambdaHelper.getQueryStringParam(event, 'beta_slider_value', LambdaHelper.valueTypeFloat) 
    E1_slider_value = LambdaHelper.getQueryStringParam(event, 'E1_slider_value', LambdaHelper.valueTypeFloat) 
    E2_slider_value = LambdaHelper.getQueryStringParam(event, 'E2_slider_value', LambdaHelper.valueTypeFloat) 
    C1_slider_value = LambdaHelper.getQueryStringParam(event, 'C1_slider_value', LambdaHelper.valueTypeFloat) 
    C2_slider_value = LambdaHelper.getQueryStringParam(event, 'C2_slider_value', LambdaHelper.valueTypeFloat) 
    h1_slider_value = LambdaHelper.getQueryStringParam(event, 'h1_slider_value', LambdaHelper.valueTypeFloat) 
    h2_slider_value = LambdaHelper.getQueryStringParam(event, 'h2_slider_value', LambdaHelper.valueTypeFloat) 
    return Synergy.calculatePlot(action=action, E0=E0, alpha12_slider_value=alpha12_slider_value,  alpha21_slider_value=alpha21_slider_value, gamma12_slider_value=gamma12_slider_value,  gamma21_slider_value=gamma21_slider_value, beta_slider_value=beta_slider_value,  E1_slider_value=E1_slider_value,  E2_slider_value=E2_slider_value, C1_slider_value=C1_slider_value,  C2_slider_value=C2_slider_value,h1_slider_value=h1_slider_value, h2_slider_value=h2_slider_value)
