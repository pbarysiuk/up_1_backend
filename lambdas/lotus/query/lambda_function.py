import json
from os import environ
import re
from bson.objectid import ObjectId
from bson.json_util import dumps
from src.shared.database import Database
from src.shared.generalWrapper import GeneralWrapper
import pymongo
import traceback
import mysql.connector
import numpy as np

from json import loads

class LambdaHelper:

    valueTypeString = 'string'
    valueTypeInt = 'int'
    valueTypeFloat = 'float'
    
    @staticmethod
    def __getValue(event, parentKey, key, type, defaultValue):
        if event.get(parentKey) is None:
            return defaultValue
        value = event[parentKey].get(key)
        if value is None:
            return defaultValue
        if type == LambdaHelper.valueTypeFloat:
            return float(value)
        elif type == LambdaHelper.valueTypeInt:
            return int(value)
        return value

    @staticmethod
    def getQueryStringParam(event, key, type = 'string', defaultValue = None):
        return LambdaHelper.__getValue(event, 'queryStringParameters', key, type, defaultValue)
    
    @staticmethod 
    def getPathParam(event, key, type = 'string'):
        return LambdaHelper.__getValue(event, 'pathParameters', key, type, None)

    @staticmethod
    def getBodyParams(event, keys):
        if event.get('body') is None:
            result = {}
            for key in keys:
                result[key] = None
            return result
        body = loads(event['body'])
        result = {}
        for key in keys:
            result[key] = body.get(key)
        return result

        
        
def lambda_handler(event, context):
    action = LambdaHelper.getPathParam(event, 'proxy')
    type = LambdaHelper.getQueryStringParam(event, 'type')
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
    return Synergy.calculatePlot(action=action, type=type, E0=E0, alpha12_slider_value=alpha12_slider_value,  alpha21_slider_value=alpha21_slider_value, gamma12_slider_value=gamma12_slider_value,  gamma21_slider_value=gamma21_slider_value, beta_slider_value=beta_slider_value,  E1_slider_value=E1_slider_value,  E2_slider_value=E2_slider_value, C1_slider_value=C1_slider_value,  C2_slider_value=C2_slider_value,h1_slider_value=h1_slider_value, h2_slider_value=h2_slider_value)
    
                                          


class Synergy:
    def _get_beta(self, E0, E1, E2, E3):
        minE = min(E1, E2)
        return (minE-E3)/(E0-minE)

    def _get_E3(self, E0, E1, E2, beta):
        minE = min(E1, E2)
        return minE - beta*(E0-minE)


    def _hill_inv(self, E, E0, Emax, h, C):
        E_ratio = (E-E0)/(Emax-E)
        d = np.float_power(E_ratio, 1./h)*C
        d[E_ratio<0] = np.nan
        return d

    def _hill_E(self, d, E0, Emax, h, C):
        dh = np.power(d,h)
        return E0 + (Emax-E0)*dh/(np.power(C,h)+dh)

    def _MuSyC_E(self, d1, d2, E0, E1, E2, E3, h1, h2, C1, C2, alpha12, alpha21, gamma12, gamma21):
        d1h1 = np.power(d1,h1)
        d2h2 = np.power(d2,h2)
        C1h1 = np.power(C1,h1)
        C2h2 = np.power(C2,h2)
        r1 = 100/C1h1
        r2 = 100/C2h2
        U=(r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)/(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*r1*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*C2h2+d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d1h1*np.power(r1,(gamma21+1))*np.power(r2,gamma12)*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r1,(gamma21+1))*r2*np.power(alpha21*d1, gamma21*h1)*C1h1+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*np.power(r2,(gamma12+1))*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)
        A1=(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12))/(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*r1*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*C2h2+d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d1h1*np.power(r1,(gamma21+1))*np.power(r2,gamma12)*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r1,(gamma21+1))*r2*np.power(alpha21*d1, gamma21*h1)*C1h1+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*np.power(r2,(gamma12+1))*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)
        A2=(d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21))/(d1h1*r1*r2*np.power((r1*C1h1),gamma21)*C2h2+d1h1*r1*r2*np.power((r2*C2h2),gamma12)*C2h2+d1h1*r1*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*C2h2+d1h1*r1*np.power(r2,gamma12)*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+d1h1*np.power(r1,(gamma21+1))*np.power(r2,gamma12)*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d1h1*np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*r1*r2*np.power((r1*C1h1),gamma21)*C1h1+d2h2*r1*r2*np.power((r2*C2h2),gamma12)*C1h1+d2h2*np.power(r1,(gamma21+1))*r2*np.power(alpha21*d1, gamma21*h1)*C1h1+d2h2*np.power(r1,gamma21)*r2*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)+d2h2*np.power(r1,gamma21)*np.power(r2,(gamma12+1))*np.power(alpha21*d1, gamma21*h1)*np.power(alpha12*d2, gamma12*h2)+d2h2*np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)+r1*r2*np.power((r1*C1h1),gamma21)*C1h1*C2h2+r1*r2*np.power((r2*C2h2),gamma12)*C1h1*C2h2+np.power(r1,(gamma21+1))*np.power(alpha21*d1, gamma21*h1)*np.power((r2*C2h2),gamma12)*C1h1+np.power(r2,(gamma12+1))*np.power(alpha12*d2, gamma12*h2)*np.power((r1*C1h1),gamma21)*C2h2)
        return U*E0 + A1*E1 + A2*E2 + (1-(U+A1+A2))*E3

    def _bliss(self, d1, d2, E, E0, E1, E2, h1, h2, C1, C2):
        E1_alone = self._hill_E(d1, E0, E1, h1, C1)
        E2_alone = self._hill_E(d2, E0, E2, h2, C2)
        synergy = E1_alone*E2_alone - E
        synergy[(d1==0) | (d2==0)] = 0
        return synergy

    def _loewe(self, d1, d2, E, E0, E1, E2, h1, h2, C1, C2):
        with np.errstate(divide='ignore', invalid='ignore'):
            d1_alone = self._hill_inv(E, E0, E1, h1, C1)
            d2_alone = self._hill_inv(E, E0, E2, h2, C2)
            synergy = d1/d1_alone + d2/d2_alone
        synergy[(d1==0) | (d2==0)] = 1
        return synergy

    def get_plot(self, d1, d2, E, bs, ls, clim=None, center_on_zero=False):
        d1[d1==0] = min(d1[d1>0])/10
        d2[d2==0] = min(d2[d2>0])/10
        d1 = np.log10(d1)
        d2 = np.log10(d2)
        sorted_indices = np.lexsort((d1,d2))
        d1 = d1[sorted_indices]
        d2 = d2[sorted_indices]   
        n_d1 = len(np.unique(d1))
        n_d2 = len(np.unique(d2))
        d1 = d1.reshape(n_d2,n_d1)
        d2 = d2.reshape(n_d2,n_d1) 
        '''
        if clim is None:
            if center_on_zero:
                cmin, cmax = -0.4,0.4
            else:
                cmin, cmax = 0,1
        else:
            cmin, cmax = clim
        '''  
        z = None
        if self.type == 'E':
            E = E[sorted_indices]
            E = E.reshape(n_d2,n_d1)
            z = E.tolist()
        elif self.type == 'ls':
            ls = ls[sorted_indices]
            ls = ls.reshape(n_d2,n_d1)
            z = ls.tolist()
        elif self.type == 'bs':
            bs = bs[sorted_indices]
            bs = bs.reshape(n_d2,n_d1)
            z = bs.tolist()
        data_to_plot = {
            "alpha12_slider_value" : self.alpha12_slider_value,
            "alpha21_slider_value" : self.alpha21_slider_value,
            "gamma12_slider_value" : self.gamma12_slider_value,
            "gamma21_slider_value" : self.gamma21_slider_value,
            "beta_slider_value" : self.beta_slider_value,
            "E1_slider_value" : self.E1_slider_value,
            "E2_slider_value" : self.E2_slider_value,
            "C1_slider_value" : self.C1_slider_value,
            "C2_slider_value" : self.C2_slider_value,
            "h1_slider_value" : self.h1_slider_value,
            "h2_slider_value" : self.h2_slider_value,
            #'x' : d1.tolist(),
            #'y' : d2.tolist(),
            'z' : z,
            #'cmin' : cmin,
            #'cmax' : cmax
        }
        return data_to_plot

    def __init__(self, action, type = 'E', E0=1, alpha12_slider_value=0.0, alpha21_slider_value=0.0, gamma12_slider_value=0.0, gamma21_slider_value=0.0, beta_slider_value=0.0, E1_slider_value=0.4, E2_slider_value=0.5, C1_slider_value=0.0, C2_slider_value=0.0, h1_slider_value=0.3, h2_slider_value=-0.3):
        self.type = type
        self._E0 = E0
        self.alpha12_slider_value = alpha12_slider_value
        self.alpha21_slider_value = alpha21_slider_value
        self.gamma12_slider_value = gamma12_slider_value
        self.gamma21_slider_value = gamma21_slider_value
        self.beta_slider_value = beta_slider_value
        self.E1_slider_value = E1_slider_value
        self.E2_slider_value = E2_slider_value
        self.C1_slider_value = C1_slider_value
        self.C2_slider_value = C2_slider_value
        self.h1_slider_value = h1_slider_value
        self.h2_slider_value = h2_slider_value
        
        
        self._beta = self.beta_slider_value
        self._E1 = self.E1_slider_value
        self._E2 = self.E2_slider_value
        self._E3 = self._get_E3(self._E0, self._E1, self._E2, self._beta)
        
        
        if action == 'resetToDefault':
            self.alpha12_slider_value=0
            self.alpha21_slider_value=0
            self.gamma12_slider_value=0
            self.gamma21_slider_value=0
        elif action == 'resetToBliss':
            self.alpha12_slider_value=0
            self.alpha21_slider_value=0
            self.gamma12_slider_value=0
            self.gamma21_slider_value=0
            self._E3 = self._E1*self._E2
            self.beta_slider_value=self._get_beta(E0, self._E1, self._E2, self._E3)
            self._beta = self.beta_slider_value
        elif action == 'resetToLoewe':
            self.h1_slider_value=0
            self.h2_slider_value=0
            self.alpha12_slider_value=-3
            self.alpha21_slider_value=-3


        elif action == 'resetToMusyc':
            self.beta_slider_value=0
            self._beta = self.beta_slider_value
            self.alpha12_slider_value=0
            self.alpha21_slider_value=0
            self.gamma12_slider_value=0
            self.gamma21_slider_value=0


        self._alpha12 = np.power(10., self.alpha12_slider_value)
        self._alpha21 = np.power(10., self.alpha21_slider_value)
        self._gamma12 = np.power(10., self.gamma12_slider_value)
        self._gamma21 = np.power(10., self.gamma21_slider_value)
        if self._alpha12==np.power(10., -3): self._alpha12=0
        if self._alpha21==np.power(10., -3): self._alpha21=0
        self._C1 = np.power(10., self.C1_slider_value)
        self._C2 = np.power(10., self.C2_slider_value)
        self._h1 = np.power(10., self.h1_slider_value)
        self._h2 = np.power(10., self.h2_slider_value)
        

        d1 = np.logspace(-3,3,30)
        d2 = np.logspace(-3,3,30)
        d1 = np.hstack([[0],d1])
        d2 = np.hstack([[0],d2])
        d1,d2 = np.meshgrid(d1, d2)
        d1 = d1.flatten()
        d2 = d2.flatten()
        self.d1 = d1
        self.d2 = d2
        self.E = self._MuSyC_E(self.d1, self.d2, self._E0, self._E1, self._E2, self._E3, self._h1, self._h2, self._C1, self._C2, self._alpha12, self._alpha21, self._gamma12, self._gamma21)
        self.bs = None
        self.ls = None
        if self.type == 'bs':
            self.bs = self._bliss(self.d1, self.d2, self.E, self._E0, self._E1, self._E2, self._h1, self._h2, self._C1, self._C2)
        if self.type == 'ls':
            with np.errstate(divide='ignore', invalid='ignore'):
                self.ls = -np.log(self._loewe(self.d1, self.d2, self.E, self._E0, self._E1, self._E2, self._h1, self._h2, self._C1, self._C2))
        self.E[np.isnan(self.E)] = 0
        #self._setup_figs()
        #self._setup_widget()

    @staticmethod
    def calculatePlot(action, type, E0, alpha12_slider_value, alpha21_slider_value, gamma12_slider_value, gamma21_slider_value, beta_slider_value, E1_slider_value, E2_slider_value, C1_slider_value, C2_slider_value, h1_slider_value, h2_slider_value):
        if E0 is None:
            E0 = 1
        if type is None:
            type = 'E'
        if alpha12_slider_value is None:
            alpha12_slider_value = 0.0
        if alpha21_slider_value is None:
            alpha21_slider_value = 0.0
        if gamma12_slider_value is None:
            gamma12_slider_value = 0.0
        if gamma21_slider_value is None:
            gamma21_slider_value = 0.0
        if beta_slider_value is None:
            beta_slider_value = 0.0
        if E1_slider_value is None:
            E1_slider_value = 0.4
        if E2_slider_value is None:
            E2_slider_value = 0.5
        if C1_slider_value is None:
            C1_slider_value = 0.0
        if C2_slider_value is None:
            C2_slider_value = 0.0
        if h1_slider_value is None:
            h1_slider_value = 0.3
        if h2_slider_value is None:
            h2_slider_value = -0.3
        try :
            plot = Synergy(action, type, E0, alpha12_slider_value, alpha21_slider_value, gamma12_slider_value, gamma21_slider_value, beta_slider_value, E1_slider_value, E2_slider_value, C1_slider_value, C2_slider_value, h1_slider_value, h2_slider_value)
            return GeneralWrapper.successResult(plot.get_plot(plot.d1, plot.d2, plot.E, plot.bs, plot.ls))
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)































def lambda_handler___(event, context):
    #return createFullTextIndex(create = False)
    db = event['pathParameters']['proxy']
    user_query = event['queryStringParameters']['query']
    return query(user_query, 0, None)
    pageSize = 100
    if db == 'sql':
        return querySql(user_query, pageSize)
    if db == 'sqlindex':
        return querySqlIndex(user_query, pageSize)
    if db == 'catNew':
        return drugbank_drugs_by_category_new(user_query, 0)
    if db == 'cat':
        return drugbank_drugs_by_category(user_query, 0)
    return queryNoSql(user_query, pageSize)




def queryNoSql(user_query, pageSize):
    try:
        dbConnection = pymongo.MongoClient(environ.get("MONGODB_CONNSTRING"))
        db = dbConnection.drugbank
        #db.xdl.drop()
        #db.xdl_list.drop()
        molecules = db.molecules.find({
            "name" : {
                "$regex": user_query,
                "$options": "i"
            }
        }, {"name" : 1, "smiles" : 1, '_id' : 0}).limit(pageSize)
        result = list(molecules)
        dbConnection.close()
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)



def drugbank_drugs_by_category(category_id, page):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        where_query = {
            "categories.drugbank_id": category_id
        }
        drugs = db.drugs.find(filter=where_query, projection={'name' : 1}).skip(page * 10).limit(10)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)
        

def drugbank_drugs_by_category_new(category_id, page):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        category = db.categories_details.find_one({'drugbank_id' : category_id}, {'drugs' : 1})
        where_query = {
            "name": {"$in" : category['drugs']}
        }
        drugs = db.drugs.find(where_query).skip(page * 10).limit(10)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)
        
        

def query(user_query: str, page: int, category: str):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        columns = ["drugbank_id", "name"]
        or_query = {
            '$or': [
                {
                    "clinical_description": {
                        "$regex": '^' + user_query,
                        "$options": "i"
                    }
                },
                {
                    "name": {
                        "$regex": '^' + user_query,
                        "$options": "i"
                    }
                },
                {
                    "synonyms.synonym": {
                        "$regex": '^' + user_query,
                        "$options": "i"
                    }
                }
            ]
        }
        where_query = {
            "$and": [
                or_query,
            ],
        }
        hint = None
        if category is not None:
            where_query["$and"].append({"categories.drugbank_id": category})
            hint = [('categories.drugbank_id', pymongo.ASCENDING)]
        drugs = None
        drugs = db.drugs_list.find(where_query, hint = hint).skip(page * 10).limit(10)
        count = db.drugs_list.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)
