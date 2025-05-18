import pandas as pd
from pydataxm.pydatasimem import ReadSIMEM
from typing import Dict
from datetime import date
import os

# Minimum date to get data
minimun_date = date(2013, 1, 1)


class DataSIMEM:
    """
    Class to retrieve and process data from SIMEM.
    
    Attributes:
        data_sets_keys (Dict[str,str]): Default dataset to get data with the names to save the files.
        data_sets (Dict[str, pd.DataFrame]): Dictionary to handel the data.

    Methods:
        _clean_data: Cleans the raw SIMEM data.
        get_simem_data: Returns the cleaned SIMEM data.
        save_simem_data: Saves the cleaned SIMEM data to an Excel file.
    """

    def __init__(self, data_sets: Dict[str, pd.DataFrame] = None) -> None:
        """
        Initialize the DataSIMEM object.

        Args:
            data_sets (Dict[str, pd.DataFrame], optional): Dictionary to store the data sets. Defaults to None.
        """
        self.data_sets_keys = {
            'B0E933': 'ReservasHidraulicasEnergía',
            'A0CF2A': 'ListadoEmbalses',
            'BA1C55': 'AportesHidricos'
        }
        self.data_sets = data_sets if data_sets else {}
        self.raw_data = {}

    def get_simem_data(self, start_date: date = None, end_date: date = None, data_sets: list = None) -> Dict[str, pd.DataFrame]:
        """
        Retrieve data from SIMEM.

        Args:
            start_date (date, optional): Start date of the data. Defaults to None.
            end_date (date, optional): End date of the data. Defaults to None.
            data_sets (list, optional): List of data sets to retrieve. Defaults to None.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing the retrieved data sets.
        """
        # Set parameters of date filters
        start_date = start_date if start_date else minimun_date
        end_date = end_date if end_date else date(date.today().year, date.today().month, 1)

        # Settings which data sets get the data
    
        data_sets = [data for data in self.data_sets_keys if data in data_sets] if data_sets is not None else self.data_sets_keys
        self.data_sets_keys = data_sets
       
        
        for data_id in data_sets:
            
            # Getting the data from the DataSet
            file = ReadSIMEM(data_id, str(start_date), str(end_date))
            data = file.main(filter=False)
            
            # Updating the Key in the Dict of DataSet's
            self.data_sets[data_id] = data
            self.raw_data[data_id] = data

        return self.data_sets

    def _clean_data(self) -> Dict[str, pd.DataFrame]:
        """
        Clean the retrieved data.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing the cleaned data sets.
        """
        if not self.data_sets:
            self.get_simem_data()
        
       
        # Setting columns from Aportes hidrios
        self.data_sets['BA1C55'] = self.data_sets['BA1C55'].drop(columns=['FechaPublicacion'])
        
        # Filtering the data
        self.data_sets['BA1C55'] = self.data_sets['BA1C55'][self.data_sets['BA1C55']['CodigoSerieHidrologica']!='Colombia']
        
        # Setting columns from Reservas hidricas
        self.data_sets['B0E933'] = self.data_sets['B0E933'].drop(columns=['FechaPublicacion'])
        
        # Filtering the data
        self.data_sets['B0E933'] = self.data_sets['B0E933'][~self.data_sets['B0E933']['CodigoEmbalse'].str.contains('AGREGADO')]

        # Setting columns from Listado embalses
        self.data_sets['A0CF2A'] = self.data_sets['A0CF2A'].drop(columns=['Fecha','FechaEjecucion'])
        
        # Dropping duplicates
        self.data_sets['A0CF2A'] = self.data_sets['A0CF2A'].drop_duplicates()

        return self.data_sets

    def save_simem_data(self, relative_path: str,save_raw:bool =False) -> Dict[str, pd.DataFrame]:
        """
        Save the retrieved data to Excel files.

        Args:
            relative_path (str): Relative path to save the data files.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing the saved data sets.
        """

        self._clean_data()

        
        for file_name in self.data_sets:
            
            file_path = os.path.abspath(os.path.join(relative_path+'\\Cleansed\\SIMEM', f'{self.data_sets_keys[file_name]}.xlsx'))
            # Save the data in the path
            self.data_sets[file_name].to_excel(file_path,index=False)
            if save_raw:
                raw_file_path = os.path.join(relative_path+'\\Raw\\SIMEM', f'{self.data_sets_keys[file_name]}.xlsx')
                self.raw_data[file_name].to_excel(raw_file_path,index=False)
        
        return self.data_sets


if __name__ == "__main__":
    import os
    start_date = date(2013, 1, 1)
    end_date = date(2025, 3, 31)
    data_sets = {
            'B0E933': pd.read_excel(os.path.abspath('./Data/Raw/SIMEM/ReservasHidraulicasEnergía.xlsx')),
            'A0CF2A': pd.read_excel(os.path.abspath('./Data/Raw/SIMEM/ListadoEmbalses.xlsx')),
            'BA1C55': pd.read_excel(os.path.abspath('./Data/Raw/SIMEM/AportesHidricos.xlsx'))
        }
    simem = DataSIMEM(data_sets=data_sets)
    simem.save_simem_data('Data')
    
