from PIL import Image
import numpy as np
from numpy.fft import fft2, fftshift
from scipy.signal import convolve2d
from math import factorial as ft #saving characters
import matplotlib.pyplot as plt

class Aberration:
    def __init__(self, m: int, n: int, plots: bool = False):
        #indexes the polynomial
        self.n = n
        self.m = m # can be positive (even zernike) or negative (odd zernike)
        #TODO just have the psf made on init with plots toggleable
        self.plots = plots
    
    def _radial_polynomial(self, r: float): #r
        
        _n = self.n
        _m = abs(self.m) #odd zernike polynomial
        
        if (_n - _m) % 2 != 0: return 0 # odd n-m has radial coeff 0
        
        rad_total = 0
        for k in range(int((_n - _m)/2 + 1)): #k is a dummy variable
            coeff = ((-1) ** k * ft(_n-k)) / (ft(k) * ft((_n + _m)//2 - k) * ft((_n - _m)//2 - k))
            term = coeff * r ** (_n - 2*k)
            rad_total += term
        
        return rad_total 
            
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

        if self.plots:
            plt.imshow(z, cmap='seismic', extent=[-l/2, l/2, -w/2, w/2])
            plt.colorbar()
            plt.title(f"Zernike mode n={self.n}, m={self.m}")
            plt.show()
        
        return z
    
    def _psf(self, w: int, l: int): #generate the point spread function of the aberrated pupil
        
        kern = self._kernel(w, l) #phase map 
        pupil = np.exp(1j * kern) #aberrated pupil function
        psf = np.abs(fftshift(fft2(pupil))) ** 2 #no need to shift kernel b4 fft bc we constructed it centered at zero above
        
        if self.plots:
            plt.imshow(psf, cmap='seismic')
            plt.colorbar()
            plt.title(f"Zernike mode n={self.n}, m={self.m}")
            plt.show()
        
        return psf / np.sum(psf)
    
    def to_grayscale(self, img): 
        return np.dot(img[:, :, :3], [0.2989, 0.5870, 0.1140]) #standard luminance formula from rgb
    
    def _convolve(self,psf, img_path: str ):
        
        img = Image.open(img_path)
        img_arr = np.array(img)
        
        grey = self.to_grayscale(img_arr) #TODO make this work with 3 channel RGB. need to convolve with each color freq

        processed = convolve2d(grey, psf, mode="same", boundary="fill")
        fig, axes = plt.subplots(1, 2, figsize=(8, 4))

        axes[0].imshow(grey, cmap='gray')
        axes[0].set_title("Unprocessed")

        axes[1].imshow(processed, cmap='gray')
        axes[1].set_title("Processed")

        plt.tight_layout()
        plt.show()
    
        
if __name__ == "__main__":
    ab = Aberration(1, 3, plots= True) #m, n #TODO i wonder how i'll manage combos?
    psf = ab._psf(256, 256)
    ab._convolve(psf, img_path="in/hq720.jpg")