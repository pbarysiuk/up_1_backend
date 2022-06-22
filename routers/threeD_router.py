from flask import  request
from urllib.parse import unquote
from src.threeDimPlot.synergy import Synergy

def init_router(flaskApp):
    @flaskApp.route('/3d/<string:action>', methods=['get'])
    def getThreeD(action):
        args = request.args
        return Synergy.calculatePlot(action=action, E0=args.get("E0", default=None, type=float), \
            alpha12_slider_value=args.get("alpha12_slider_value", default=None, type=float), \
                 alpha21_slider_value=args.get("alpha21_slider_value", default=None, type=float), \
                     gamma12_slider_value=args.get("gamma12_slider_value", default=None, type=float), \
                         gamma21_slider_value=args.get("gamma21_slider_value", default=None, type=float), \
                             beta_slider_value=args.get("beta_slider_value", default=None, type=float), \
                                 E1_slider_value=args.get("E1_slider_value", default=None, type=float), \
                                     E2_slider_value=args.get("E2_slider_value", default=None, type=float), \
                                         C1_slider_value=args.get("C1_slider_value", default=None, type=float), \
                                         C2_slider_value=args.get("C2_slider_value", default=None, type=float),\
                                          h1_slider_value=args.get("h1_slider_value", default=None, type=float),\
                                          h2_slider_value=args.get("h2_slider_value", default=None, type=float))
        #data = request.get_json(force=True)
        #return XdlBusiness.add(drugs = data["drugs"], filePath=data["filePath"])