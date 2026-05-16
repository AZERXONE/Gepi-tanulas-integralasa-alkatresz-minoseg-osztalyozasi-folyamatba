import pandas as pd
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

class FeaturePreprocesser:

    def __ini__(self):
        pass

    def process(self, data_df, num_of_points, num_of_surface_measurements):

        results_df = pd.DataFrame(columns=['num_of_peaks',
                                           'num_of_troughs',
                                           'max_num_of_peaks',
                                           'max_num_of_troughs',
                                           'min_num_of_peaks',
                                           'min_num_of_troughs',
                                           'max_peak',
                                           'max_trough',
                                           'min_peak',
                                           'min_troughs',
                                           'max_area_between',
                                           'min_area_between',
                                           'avarage_area_between',
                                           'avarage_extra_material',
                                           'min_extra_material',
                                           'max_extra_material',
                                           'Gear_ID',
                                           'Date'
                                           ])
        
        for gear in range(data_df.shape[0]):

            features = []

            for i in range(num_of_surface_measurements):

                new_features = []

                datas = data_df.iloc[gear][num_of_points * i:num_of_points * (i+1)]
                metadata = data_df.iloc[gear][['Gear_ID','Date']]
        
                x = range(len(datas))
                x = np.array(x).reshape(-1, 1)

                polynomial = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
                polynomial.fit(x[43:453], datas[43:453])
                y_fit = polynomial.predict(x)

                area = np.trapezoid(np.abs(datas - y_fit), x.flatten())

                peaks, p_properties = find_peaks(datas)
                troughs, t_properties = find_peaks(-datas)

                if len(peaks):
                    p_max = np.array([(datas[peak] - y_fit[peak]) for peak in peaks]).max()
                    p_min = np.array([(datas[peak] - y_fit[peak]) for peak in peaks]).min()
                else:
                    p_max = 0
                    p_min = 0
                if len(troughs):
                    t_max = np.array([(datas[trough] - y_fit[trough]) for trough in troughs]).max()
                    t_min = np.array([(datas[trough] - y_fit[trough]) for trough in troughs]).min()
                else:
                    t_max = 0
                    t_min = 0

                extra_mat = abs(y_fit[0] - datas[-1])

                new_features.append(len(peaks))
                new_features.append(len(troughs))
                
                new_features.append(p_max)
                new_features.append(t_max)
                new_features.append(p_min)
                new_features.append(t_min)
                
                new_features.append(area)
                
                new_features.append(extra_mat)

                features.append(new_features)

            features = np.array(features)

            num_of_peaks = features[:,0].sum()
            num_of_troughs = features[:,1].sum()
            max_num_of_peaks = features[:,0].max()
            max_num_of_troughs = features[:,1].max()
            min_num_of_peaks = features[:,0].min()
            min_num_of_troughs = features[:,1].min()
            max_peak = np.nanmax(features[:,2])
            max_trough = np.nanmax(features[:,3])
            min_peak = np.nanmin(features[:,4])
            min_trough = np.nanmin(features[:,5])
            avarage_area_between = features[:,6].mean()
            max_area_between = features[:,6].max()
            min_area_between = features[:,6].min()
            avarage_extra_mat = features[:,7].mean()
            max_extra_mat = features[:,7].max()
            min_extra_mat = features[:,7].min()

            new_row = {
                'num_of_peaks' : num_of_peaks,
                'num_of_troughs' : num_of_troughs,
                'max_num_of_peaks' : max_num_of_peaks,
                'max_num_of_troughs' : max_num_of_troughs,
                'min_num_of_peaks' : min_num_of_peaks,
                'min_num_of_troughs' : min_num_of_troughs,
                'max_peak' : max_peak,
                'max_trough' : max_trough,
                'min_peak' : min_peak,
                'min_troughs' : min_trough,
                'max_area_between' : max_area_between,
                'min_area_between' : min_area_between,
                'avarage_area_between' : avarage_area_between,
                'min_extra_material' : min_extra_mat,
                'avarage_extra_material' : avarage_extra_mat,
                'max_extra_material' : max_extra_mat,
                'Gear_ID' : metadata['Gear_ID'],
                'Date' : metadata['Date']
            }

            results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)

            return results_df
