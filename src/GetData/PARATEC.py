import requests
import urllib3
import pandas as pd
import datetime
import json

# API to get reservoirs data
url_paratect = "https://paratecbackend.xm.com.co/reportehidrologia/api/Hydrology/ReservoirInfo"

# Disclable warning for SSL certificate of PARATEC
urllib3.disable_warnings()


class DataPARATEC:
    """
    Class for retrieving and processing reservoirs data from PARATEC.
    
    Attributes:
        data_raw (pandas.DataFrame): Raw reservoirs data.
        data (pandas.DataFrame): Cleaned reservoirs data.

    Methods:
        _clean_data: Cleans the raw reservoirs data.
        get_paratec_data: Returns the cleaned reservoirs data.
        save_paratec_data: Saves the cleaned reservoirs data to an Excel file.
    """

    def __init__(self) -> None:
        # Reading the data
        self.data_raw = requests.request("GET", url_paratect, verify=False).json()
        self.data = None
    
    def _clean_data(self)->pd.DataFrame:
        """
        Cleans the raw data and prepares it for further processing.
        
        Returns:
            pandas.DataFrame: Cleaned reservoirs data.
        """
        
        # Get data from 'data' key
        data = pd.DataFrame(self.data_raw['data'])
        
        # Mapping boolean column to number
        data['isReservoirAggregate'] = data['isReservoirAggregate'].map({'Si': 1, 'No': 0})
        
        # Selecting columns
        data = data[['reservoir', 'latitude', 'longitude']]
        
        # removing aggregates from reservoirs (those with NaN latitude)
        data = data[~data['latitude'].isnull()]
        self.data = data
        return self.data
    
    def get_paratec_data(self)->pd.DataFrame:
        """
        Retrieves the PARATEC data.

        Returns:
            pandas.DataFrame: Cleaned reservoirs data.
        """
        if not self.data:
            # Clean the data
            self._clean_data()
        return self.data
    
    def save_paratec_data(self, path: str,save_raw:bool=False)->pd.DataFrame:
        """
        Saves the PARATEC data to a specified path.

        Args:
            path (str): The file path to save the data.

        Returns:
            pandas.DataFrame: Cleaned reservoirs data.
        """
        if self.data is None:
            # Clean the data
            self._clean_data()
        
        if save_raw:
            with open(path, 'w') as file:
                json.dump(self.data_raw, file)
                
            return self.data_raw    
        
        try:
            # Save the data in the path
            self.data.to_excel(path,index=False)
        except Exception as e:
            print(f"Error al guardar los datos en la ruta {path}: {e}")
        else:
            return self.data
           
        
if __name__ == '__main__':
    paratec = DataPARATEC()
    today = datetime.date.today()
    filename_cleansed = f'Data/Cleansed/PARATEC/PARATEC_{today}.xlsx'
    filename_raw = f'Data/Raw/PARATEC/PARATEC_{today}.xlsx'
    paratec.save_paratec_data(filename_cleansed)
    paratec.save_paratec_data(filename_raw, save_raw=True)
