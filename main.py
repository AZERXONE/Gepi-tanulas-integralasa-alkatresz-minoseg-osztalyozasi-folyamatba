import pandas as pd
import numpy as np
import joblib

from feature_preprocessing import FeaturePreprocesser
from postprocessing import PostProcess
from functions import printMessage, toCSV
import warnings
warnings.filterwarnings('ignore')

def main() -> None:

    try:
        printMessage("AI stamper started")

        df = pd.read_csv("test.csv").iloc[[12]]

        feature_preprocesser = FeaturePreprocesser()

        feature_df = feature_preprocesser.process(df, 400, 16)

        columns_to_exclude = ['Gear_ID','Date']

        model = joblib.load("VotingCL.pkl")
        scaler = joblib.load("MinMaxScaler.pkl")

        X = feature_df.drop(columns=columns_to_exclude)
        X_scaled = scaler.transform(X)
        
        X = pd.DataFrame(
            X_scaled,
            columns=X.columns,
            index=X.index
        )

        y_pred_proba = model.predict_proba(X)
        decision_boundary = 0.5

        X_result = {
            'Gear_ID': feature_df['Gear_ID'],
            'Date': feature_df['Date'],
            'Predicted_label': np.where(y_pred_proba[:,1] >= decision_boundary, "A1", "!A1"),
            '!A1_confidence' :round(y_pred_proba[0][0],3),
            'A1_confidence': round(y_pred_proba[0][1],3),
            'Security_layer_triggered': 'False'
        }

    except Exception as e:
            printMessage(f"Processing Error : {e}")
    
    try:
        if X_result['Predicted_label'] == 'A1':
            
            postprocesser = PostProcess()
            post_check = postprocesser.check(X)
            if not post_check:
                X_result['Security_layer_triggered'] = 'True'
                X_result['Predicted_label'] = '!A1'
                printMessage("Security layer triggered")
    except Exception as e:
         printMessage(f"Postprocessing error : {e}")

    toCSV(pd.DataFrame(X_result))
    printMessage("AI stamper terminated")

if __name__ == '__main__':
     main()