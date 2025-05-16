import pandas as pd

# Path to get ONI Data
oni_path = 'https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt'

# Map to transform the initials of the months of the average of the data in the number of the middle month
seas_to_month = {
    'DJF': 1, 'JFM': 2, 'FMA': 3, 'MAM': 4, 'AMJ': 5, 'MJJ': 6,
    'JJA': 7, 'JAS': 8, 'ASO': 9, 'SON': 10, 'OND': 11, 'NDJ': 12
}

class DataOni:
    """
    Class for handling ONI data.

    Attributes:
        data_raw (pandas.DataFrame): Raw ONI data.
        data (pandas.DataFrame): Cleaned ONI data.

    Methods:
        _clean_data: Cleans the raw ONI data.
        get_oni_data: Returns the cleaned ONI data.
        save_oni_data: Saves the cleaned ONI data to an Excel file.

    """

    def __init__(self) -> None:
        # Reading the data
        self.data_raw = pd.read_csv(oni_path, sep='\s+')
        self.data = None
    
    def _clean_data(self)->pd.DataFrame:
        """
        Cleans the raw ONI data.

        Returns:
            pandas.DataFrame: Cleaned ONI data.

        """
        df = self.data_raw.copy()
        
        # Applying mapping
        df['Mes'] = df['SEAS'].map(seas_to_month)
        
        # Renaming columns for better understanding
        df.rename(columns={'YR': 'Year', 'Mes': 'Month', 'TOTAL': 'SST'}, inplace=True)

        # Creating the date column based on the year and month and setting the day to the first of the month
        df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
        
        # Selected the necessary columns
        df = df[['Date','ONI','ANOM']]
        self.data = df
        return self.data
    
    def get_oni_data(self)->pd.DataFrame:
        """
        Returns the cleaned ONI data.

        Returns:
            pandas.DataFrame: Cleaned ONI data.

        """
        if not self.data:
            # Clean the data
            self._clean_data()
        return self.data
    
    def save_oni_data(self, path: str)-> pd.DataFrame:
        """
        Saves the cleaned ONI data to an Excel file.

        Args:
            path (str): The file path to save the data.

        Returns:
            pandas.DataFrame: Cleaned ONI data.

        """
        if not self.data:
            # Clean the data
            self._clean_data()
        try:
            # Save the data in the path
            self.data.to_excel(path,index=False)
        except Exception as e:
            print(f"Error al guardar los datos en la ruta {path}: {e}")
        else:
            return self.data
    
if __name__ == '__main__':
    oni = DataOni()
    oni.save_oni_data('Data\ONI\ONI_historico.xlsx')

        