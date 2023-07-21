from datacube.virtual import construct, Transformation, Measurement
import xarray as xr
import numpy as np
import copy
import pickle
import sys
sys.path.append("/home/jovyan/code/dea-notebooks/Tools")
from dea_tools.classification import sklearn_unflatten
from dea_tools.classification import sklearn_flatten

class woody_cover(Transformation):

    def __init__(self, model_pickle, **settings):
        """
        Takes an existing model saved out as a pickle file.
        """
        # Unpickle model
        with open(model_pickle, "rb") as f:
            self.ml_model_dict = pickle.load(f)

    def compute(self, data):
        #drop the Mad bands from best pixel GeoMad
        data = data.drop_vars(['sdev', 'edev', 'bcdev', 'count'])
        flat = sklearn_flatten(data)
        flat = flat/10000
        results = self.ml_model_dict.predict(flat)
        predicted_wcf = (sklearn_unflatten(results,data).transpose())#[0]
        return predicted_wcf.to_dataset(name='woody_cover').squeeze().drop_vars('time')

    def measurements(self, input_measurements):
        return {'woody_cover': Measurement(name='woody_cover', dtype='float32', nodata=float('nan'), units='1')}