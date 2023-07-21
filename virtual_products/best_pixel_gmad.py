from datacube.virtual import construct, Transformation, Measurement
import xarray as xr
import numpy as np
import copy
from itertools import groupby
from datacube.utils import masking
from datacube.testutils.io import rio_slurp_xarray
import datacube

class best_pixel_gmad(Transformation):
    '''
    Get best available data for annual Landsat products
    Products must be provided in the following order:
                
    collate:
        - product: ga_ls8c_nbart_gm_cyear_3
        - product: ga_ls5t_nbart_gm_cyear_3
        - product: ga_ls7e_nbart_gm_cyear_3
    '''

    def compute(self, data):
        if 0 in data.sensor.values:
            # Landsat 8
            data = data.where(data.sensor==0, drop=True)
        elif 1 in data.sensor.values:
            # Landsat 5
            data = data.where(data.sensor==1, drop=True)
        elif 2 in data.sensor.values:
            # Landsat 7
            data = data.where(data.sensor==2, drop=True)
            
        # rescale c3 edev values to match collection 2 values
        data['edev'] = (data['edev']/10000)    
            
        return data.drop(['sensor', 'time']).squeeze()

    def measurements(self, input_measurements):
        return {'best_pixel_gmad': Measurement(name='best_pixel_gmad', dtype='float32', nodata=float('nan'), units='1')}
