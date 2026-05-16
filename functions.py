import logging
from datetime import datetime
import pandas as pd

def gettime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log(message: str, log_type='info') -> None:

    if '[' in message and ']' in message: message = message[22:]

    if log_type == 'info':      logging.info(message)
    elif log_type == 'warning': logging.warning(message)
    elif log_type == 'error':   logging.error(message, exc_info=True)
    else:                       logging.info(message)

def printMessage(message: str) -> None:

    text = f"[{gettime()}] {message}"
    print(text)
    if 'exception' in message:
        log(text, 'error')
    else: log(text)

def toCSV(df: pd.DataFrame, file_path = 'results.csv') -> None:

    file_path = "results.csv"

    try:

        dataframe = pd.read_csv(file_path)

    except (pd.errors.EmptyDataError, FileNotFoundError):

        columns = ['Gear_ID', 'Date', 'Predicted_label', '!A1_confidence', 'A1_confidence','Security_layer_triggered']
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)
        dataframe = pd.read_csv(file_path)

    dataframe = pd.concat([dataframe, df], ignore_index=True)
    dataframe.to_csv(file_path, index=False)

    printMessage(f"Result saved to {file_path} | {dataframe['Predicted_label'].iloc[-1]} | {dataframe['!A1_confidence'].iloc[-1]:.3f}")