import pillow
import numpy as np
from math import factorial as ft #saving characters
import matplotlib.pyplot as plt

class Abberation:
    def __init__(self, n: int, m: int):
        #indexes the polynomial
        self.n = n
        self.m = m # can be positive (even zernike) or negative (odd zernike)
        
        if self.m == 0: 
            raise Exception("No spherical zernike polynomials!") ##
    
    def _radial_polynomial(self, r: float): #r
        
        _n = self.n
        _m = abs(self.m) #odd zernike polynomial
        
        if _n - _m % 2 != 0: return 0 # odd n-m has radial coeff 0
        
        rad_total = 0
        for k in range(0, (_n - _m)/2 + 1): #k is a dummy variable
            coeff = ((-1) ** k * ft(_n-k)) / (ft(k) * ft((_n + _m)/2 - k) * ft((_n - _m)/2 - k))
            term = coeff * r ** (_n - 2*k)
            rad_total += term
        
        return rad_total
            
    def _zernike(self, r: float, theta: float):
        if self.m > 0: #even 
            return np.cos(self.m * theta) * self._radial_polynomial(r)
        elif self.m < 0: #odd
            return np.sin(self.m * theta) * self._radial_polynomial(r)
        else:
            raise Exception("No spherical zernike polynomials!")
    
    def _kernel(self, w: int, l: int):
        pass
    
    def _convolve(self, img):
        pass