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
        self.data_sets = data_sets

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
        data_sets = [data for data in self.data_sets_keys if data in data_sets] if data_sets else self.data_sets
        self.data_sets_keys = data_sets
        
        
        for data_id in data_sets:
            
            # Getting the data from the DataSet
            file = ReadSIMEM(data_id, str(start_date), str(end_date))
            data = file.main(filter=False)
            
            # Updating the Key in the Dict of DataSet's
            self.data_sets[data_id] = data

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
        self.data_sets['BA1C55'] = self.data_sets['BA1C55'][['Fecha', 
                                                             'CodigoSerieHidrologica', 
                                                             'RegionHidrologica', 
                                                             'AportesHidricosEnergia', 
                                                             'PromedioAcumuladoEnergia', 
                                                             'MediaHistoricaEnergia']][self.data_sets['B0E933']['CodigoEmbalse']!='Colombia']

        # Setting columns from Reservas hidricas
        self.data_sets['B0E933'] = self.data_sets['B0E933'][['Fecha', 
                                                             'CodigoEmbalse', 
                                                             'RegionHidrologica', 
                                                             'VolumenUtilDiarioEnergia', 
                                                             'CapacidadUtilEnergia', 
                                                             'VolumenTotalEnergia', 
                                                             'VertimientosEnergia']]['AGREGADO' not in self.data_sets['B0E933']['CodigoEmbalse']]

        # Setting columns from Listado embalses
        self.data_sets['A0CF2A'] = self.data_sets['A0CF2A'][['CodigoEmbalse', 
                                                             'NombreEmbalse']].drop_duplicates()

        return self.data_sets

    def save_simem_data(self, relative_path: str) -> Dict[str, pd.DataFrame]:
        """
        Save the retrieved data to Excel files.

        Args:
            relative_path (str): Relative path to save the data files.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing the saved data sets.
        """
        if not self.data_sets:
            # Clean the data
            self._clean_data()

        for file_name in self.data_sets:
            try:
                file_path = os.path.join(relative_path, f'{file_name}.xlsx')
                # Save the data in the path
                self.data.to_excel(file_path,index=False)
            except Exception as e:
                print(f"Error al guardar los datos en la ruta {file_path}: {e}")

        return self.data_sets


if __name__ == "__main__":
    start_date = date(date.today().year, date.today().month, 1)
    end_date = date.today()
    simem = DataSIMEM()
    data = simem.get_simem_data(start_date=start_date, end_date=end_date)
