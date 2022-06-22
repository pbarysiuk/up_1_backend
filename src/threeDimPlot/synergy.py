from abc import ABC, abstractmethod
import numpy as np
import json
from src.shared.generalWrapper import GeneralWrapper
import traceback


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
        E = E[sorted_indices]
        bs = bs[sorted_indices]
        ls = ls[sorted_indices]
        n_d1 = len(np.unique(d1))
        n_d2 = len(np.unique(d2))
        d1 = d1.reshape(n_d2,n_d1)
        d2 = d2.reshape(n_d2,n_d1)
        E = E.reshape(n_d2,n_d1)
        bs = bs.reshape(n_d2,n_d1)
        ls = ls.reshape(n_d2,n_d1)
        '''
        if clim is None:
            if center_on_zero:
                cmin, cmax = -0.4,0.4
            else:
                cmin, cmax = 0,1
        else:
            cmin, cmax = clim
        '''     
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
            'x' : d1.tolist(),
            'y' : d2.tolist(),
            'z' : {
                'E' : E.tolist(),
                'bs' : bs.tolist(),
                'ls' : ls.tolist()
            },
            #'cmin' : cmin,
            #'cmax' : cmax
        }
        return data_to_plot

    def __init__(self, action, E0=1, alpha12_slider_value=0.0, alpha21_slider_value=0.0, gamma12_slider_value=0.0, gamma21_slider_value=0.0, beta_slider_value=0.0, E1_slider_value=0.4, E2_slider_value=0.5, C1_slider_value=0.0, C2_slider_value=0.0, h1_slider_value=0.3, h2_slider_value=-0.3):
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
        self.bs = self._bliss(self.d1, self.d2, self.E, self._E0, self._E1, self._E2, self._h1, self._h2, self._C1, self._C2)
        with np.errstate(divide='ignore', invalid='ignore'):
            self.ls = -np.log(self._loewe(self.d1, self.d2, self.E, self._E0, self._E1, self._E2, self._h1, self._h2, self._C1, self._C2))
        self.E[np.isnan(self.E)] = 0
        #self._setup_figs()
        #self._setup_widget()

    @staticmethod
    def calculatePlot(action, E0, alpha12_slider_value, alpha21_slider_value, gamma12_slider_value, gamma21_slider_value, beta_slider_value, E1_slider_value, E2_slider_value, C1_slider_value, C2_slider_value, h1_slider_value, h2_slider_value):
        if E0 is None:
            E0 = 1
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
            plot = Synergy(action, E0, alpha12_slider_value, alpha21_slider_value, gamma12_slider_value, gamma21_slider_value, beta_slider_value, E1_slider_value, E2_slider_value, C1_slider_value, C2_slider_value, h1_slider_value, h2_slider_value)
            return GeneralWrapper.successResult(plot.get_plot(plot.d1, plot.d2, plot.E, plot.bs, plot.ls))
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)




