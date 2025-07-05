#import pillow
import numpy as np
from math import factorial as ft #saving characters
import matplotlib.pyplot as plt

class Aberration:
    def __init__(self, n: int, m: int):
        #indexes the polynomial
        self.n = n
        self.m = m # can be positive (even zernike) or negative (odd zernike)
        
        if self.m == 0: 
            raise Exception("No spherical zernike polynomials!") ##
    
    def _radial_polynomial(self, r: float): #r
        
        _n = self.n
        _m = abs(self.m) #odd zernike polynomial
        
        if (_n - _m) % 2 != 0: return 0 # odd n-m has radial coeff 0
        
        rad_total = 0
        for k in range(int((_n - _m)/2 + 1)): #k is a dummy variable
            coeff = ((-1) ** k * ft(_n-k)) / (ft(k) * ft((_n + _m)/2 - k) * ft((_n - _m)/2 - k))
            term = coeff * r ** (_n - 2*k)
            rad_total += term
        
        return rad_total / np.max(np.abs(rad_total))
            
    def _zernike(self, r: float, theta: float):
        if self.m > 0: #even 
            return np.cos(self.m * theta) * self._radial_polynomial(r)
        elif self.m < 0: #odd
            return np.sin(self.m * theta) * self._radial_polynomial(r)
        else:
            return self._radial_polynomial(r)
    
    def _kernel(self, w: int, l: int): # I guess width and length are in pixels?
        x = np.linspace(-l/2, l/2, l) #each unit is a pixel
        y = np.linspace(-w/2, w/2, w)
        xval, yval = np.meshgrid(x, y, indexing="ij") #provides the coordinates of the mesh defined by x and y
        
        z = np.zeros((w,l))
        for i in range(w):
            for j in range(l):
                xcoor = xval[i, j]
                ycoor = yval[i, j]
                
                r = np.sqrt(xcoor **2 + ycoor **2 )
                theta = np.arctan2(ycoor, xcoor)
                z[i, j] = self._zernike(r, theta)
        
        print(z)
        plt.imshow(z, cmap='seismic', extent=[-l/2, l/2, -w/2, w/2])
        plt.colorbar()
        plt.title(f"Zernike mode n={self.n}, m={self.m}")
        plt.show()
            
    def _convolve(self, img):
        pass
    
if __name__ == "__main__":
    ab = Aberration(0, 2)
    ab._kernel(10, 10)