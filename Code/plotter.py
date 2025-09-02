import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
        
    def normal_parameters(self):
        """Calculate mean and std dev of data"""
        return np.mean(self.data), np.std(self.data)
    
    def plot_histogram_with_fit(self):
        """Plot histogram with normal distribution overlay"""
        # Get parameters
        mu, sigma = self.normal_parameters()
        
        # Create histogram
        plt.hist(self.data, bins='auto', density=True, 
                alpha=0.7, color='lightgreen', label='Data')
        
        # Create fitted normal curve
        x = np.linspace(min(self.data), max(self.data), 160)
        plt.plot(x, norm.pdf(x, mu, sigma), 
                'r-', linewidth=2, label='Normal Fit')
        
        plt.title(f'μ = {mu:.2f}, σ = {sigma:.2f}')
        plt.xlabel('Value')
        plt.ylabel('Density')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

