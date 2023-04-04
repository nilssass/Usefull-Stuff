import numpy as np


class Histogram:
    
    def __init__(self, hist_min, hist_max, num_bins):
        if hist_min > hist_max or hist_min == hist_max:
            raise ValueError('hist_min must be smaller than hist_max')
            
        elif not isinstance(num_bins,int) or num_bins <= 0:
            raise ValueError('Number of bins must be a positive integer')
            
        else:
            self.hist_min = hist_min
            self.hist_max = hist_max
            self.num_bins = num_bins
            self.num_events = 1
            self.histogram = np.zeros(num_bins)
        
        
    def get_histogram(self):
        return self.histogram
    
    
    def get_num_events(self):
        return self.num_events
    
    
    def get_bin_coordinates(self):
        return np.linspace(self.hist_min, self.hist_max, num=self.num_bins)
    
    
    def get_bin_width(self):
        return (self.hist_max - self.hist_min)/(self.num_bins - 1)
    
    
    def add_value(self, value):
        # Case 1.1: value is a single number
        if isinstance(value, (int, float, np.number)):
            
            if value < self.hist_min or value > self.hist_max:
                err_msg = 'Value '+str(value)+' lies outside the histogram '+\
                          'range ['+str(self.hist_min)+','+str(self.hist_max)+\
                          ']. Increase histogram range!'
                raise ValueError(err_msg)
            else:
                hist_min = self.hist_min
                hist_max = self.hist_max
                num_bins = self.num_bins
                
                bin_width = (hist_max-hist_min)/(num_bins-1)
                bin_positions = np.linspace(hist_min, hist_max, num=num_bins)
                bin_edges = np.append(bin_positions, bin_positions[-1]+bin_width)-bin_width/2
                
                for i in range(0, num_bins):
                    # Case 2.1: histogram contains only 1 event
                    if self.num_events == 1:
                        if i == 0 and value == bin_edges[0]:
                            self.histogram[0] += 1
                        elif value > bin_edges[i] and value <= bin_edges[i+1]:
                            self.histogram[i] += 1
                    # Case 2.2: If histogram contains multiple events, always add 
                    #           values to the latest event
                    else:
                        if i == 0 and value == bin_edges[0]:
                            self.histogram[-1,0] += 1
                        elif value > bin_edges[i] and value <= bin_edges[i+1]:
                            self.histogram[-1,i] += 1
            
        # Case 1.2: value is a list of numbers
        elif type(value) == list or isinstance(value, np.ndarray):
            for element in value:
                self.add_value(element)
            
        # Case 1.3: value has an invalid input type
        else:
            err_msg = 'Invalid input type! Input value must have one of the '+\
                      'following types: (int, float, np.number, list, np.ndarray)'
            raise TypeError(err_msg)

    
    def add_event(self):
        empty_histogram = np.zeros(self.num_bins)
        self.histogram = np.vstack((self.histogram, empty_histogram))
        
        self.num_events += 1
                
                    
    def get_averaged_histogram(self):
        if self.histogram.ndim == 1:
            raise TypeError('Cannot average an array of dim = 1')
        else:
            average_hist = Histogram(self.hist_min, self.hist_max, self.num_bins)
            average_hist.histogram = np.mean(self.histogram, axis=0)
            
            return average_hist
    
    
    def normalize_histogram_by(self, value):
        self.histogram /= value
        return self
    
        
    def get_std_err(self):
        if self.histogram.ndim == 1:
            raise TypeError('Cannot compute the standard error of an array of dim = 1')
        else:
            return np.std(self.histogram, axis=0)/np.sqrt(self.num_events)
