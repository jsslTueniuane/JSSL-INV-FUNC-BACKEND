import pandas as pd
import unicodedata
from sklearn.preprocessing import MinMaxScaler
from typing import List

def strip_accents(s):
    """
    Remove accents from a given string.

    Args:
    s (str): The input string with accents.

    Returns:
    str: The input string without accents.
    """
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

class JoinData:
    """
    Class to join and clean data for analysis.

    Attributes:
    - df_oni: DataFrame containing ONI historical data.
    - df_paratec: DataFrame containing PARATEC data.
    - df_simem_reservas: DataFrame containing SIMEM reservoir data.
    - df_simem_aportes: DataFrame containing SIMEM water contributions data.
    - df_simem_embalses: DataFrame containing SIMEM reservoir list.
    - scaler: MinMaxScaler for data normalization.

    Methods:
    - _clean_data(): Cleans and preprocesses the data.
    - _merge_data_not_agregate(): Merges data without aggregation.
    - _merge_data_agregate(): Merges data with aggregation.
    - save_data_not_agregate(stale: bool): Saves non-aggregated data.
    - save_data_agregate(stale: bool): Saves aggregated data.
    """
    def __init__(self):
        
        self.df_oni = pd.read_excel('D:\mis documentos\Personal\Repos\JSSL-INV-FUNC-BACKEND\Data\ONI\ONI_historico.xlsx')
        self.df_paratec = pd.read_excel('D:\mis documentos\Personal\Repos\JSSL-INV-FUNC-BACKEND\Data\PARAREC\PARATEC_2025-05-14.xlsx')
        self.df_simem_reservas = pd.read_excel('D:\mis documentos\Personal\Repos\JSSL-INV-FUNC-BACKEND\Data\SIMEM\ReservasHidraulicasEnergía.xlsx')
        self.df_simem_aportes = pd.read_excel('D:\mis documentos\Personal\Repos\JSSL-INV-FUNC-BACKEND\Data\SIMEM\AportesHidricos.xlsx')
        self.df_simem_embalses = pd.read_excel('D:\mis documentos\Personal\Repos\JSSL-INV-FUNC-BACKEND\Data\SIMEM\ListadoEmbalses.xlsx')
        self.scaler = MinMaxScaler()

    def _clean_data(self) -> List[pd.DataFrame]:
        """
        Cleans and preprocesses the dataframes.

        Returns:
        List of cleaned and preprocessed DataFrames: df_paratec, df_simem_embalses, df_oni, df_simem_reservas, df_simem_aportes.
        """
        
        # standardizing words, removing spaces and accents to join data
        self.df_paratec['reservoir'] = self.df_paratec['reservoir'].str.replace(' ', '')
        self.df_paratec['reservoir'] = self.df_paratec['reservoir'].apply(lambda x: strip_accents(x))
        self.df_simem_embalses['NombreEmbalse'] = self.df_simem_embalses['NombreEmbalse'].str.replace(' ', '')
        self.df_simem_embalses['NombreEmbalse'] = self.df_simem_embalses['NombreEmbalse'].apply(lambda x: strip_accents(x))
        
        # Creating ONI Daily Data to join with the rest of the data
        self.df_simem_reservas['Fecha'] = pd.to_datetime(self.df_simem_reservas['Fecha'])
        self.df_oni.set_index('Date', inplace=True)
        self.df_oni = self.df_oni.resample('D').ffill()
        self.df_oni.reset_index(inplace=True)
        
        # Filling missing values in df_simem_aportes
        self.df_simem_aportes['PromedioAcumuladoEnergia'].fillna(method='ffill', inplace=True)
        self.df_simem_aportes['MediaHistoricaEnergia'].fillna(method='bfill', inplace=True)
        
        return self.df_paratec, self.df_simem_embalses, self.df_oni, self.df_simem_reservas, self.df_simem_aportes
    
    def _merge_data_not_agregate(self)-> pd.DataFrame:
        """
        Merge data from different dataframes without aggregation.
        
        Returns:
        pd.DataFrame: Merged dataframe with specified columns.
        """
        
        # Join paratec data to get coordinates with CodigoEmbalse
        df_merged = self.df_paratec.merge(self.df_simem_embalses, how='left', left_on='reservoir', right_on='NombreEmbalse')
        df_merged = df_merged[['reservoir','latitude','longitude','CodigoEmbalse']].merge(self.df_simem_embalses, how='left', left_on='reservoir', right_on='CodigoEmbalse')
        df_merged['CodigoEmbalse'] = df_merged['CodigoEmbalse_x'].combine_first(df_merged['CodigoEmbalse_y'])
        df_merged = df_merged[['latitude','longitude','CodigoEmbalse']]
        
        # Join with ONI Data
        df_merge_reservas = df_simem_reservas.merge(df_oni, how='left', left_on='Fecha', right_on='Date')
        df_merge_reservas = df_merge_reservas[df_merge_reservas['Date'].notnull()].drop(columns=['Date'])

        # Join with SIMEM reservoir data with coordinates
        df_merge_res_embalses = df_merge_reservas.merge(df_merged, how='left', left_on='CodigoEmbalse', right_on='CodigoEmbalse')
        
        # Selecting columns to keep
        df_merge_res_embalses = df_merge_res_embalses[['Fecha','VolumenUtilDiarioEnergia','CapacidadUtilEnergia','VolumenTotalEnergia','VertimientosEnergia','SST','ANOM','latitude','longitude']]
        
        # Create new columns for day, month, and year
        df_merge_res_embalses['Dia'] = df_merge_res_embalses['Fecha'].dt.day
        df_merge_res_embalses['Mes'] = df_merge_res_embalses['Fecha'].dt.month
        df_merge_res_embalses['Año'] = df_merge_res_embalses['Fecha'].dt.year
        df_merge_res_embalses.drop(columns=['Fecha'], inplace=True)

        return df_merge_res_embalses
    
    def _merge_data_agregate(self)-> pd.DataFrame:
        """
        Merge data from different dataframes with aggregation.

        Returns:
        pd.DataFrame: Merged and aggregated dataframe with specified columns.
        """
        #Get general data
        df_merge_agregate = self._merge_data_not_agregate()
        
        # Aggregate data with Date and region
        df_merge_res_embalses_agregados = df_merge_agregate.groupby(['Fecha', 'RegionHidrologica']).agg({'VolumenUtilDiarioEnergia': 'mean','CapacidadUtilEnergia':'mean','VolumenTotalEnergia':'max','VertimientosEnergia':'sum','SST':'mean','ANOM':'mean'}).reset_index()

        # filling missing values in df_simem_aportes
        df_simem_aportes['PromedioAcumuladoEnergia'].fillna(method='ffill', inplace=True)
        df_simem_aportes['MediaHistoricaEnergia'].fillna(method='bfill', inplace=True)
        
        # Aggregate data with Date and region
        df_aportes_agregados = df_simem_aportes.groupby(['Fecha', 'RegionHidrologica']).agg({'AportesHidricosEnergia': 'sum','PromedioAcumuladoEnergia':'mean','MediaHistoricaEnergia':'max'}).reset_index()

        # Join dataframes on Date and region
        df_merge_res_embalses_agregados['Fecha'] = df_merge_res_embalses_agregados['Fecha'].astype(str)
        df_aportes_agregados['Fecha'] = df_aportes_agregados['Fecha'].astype(str)
        df_merge_agregate = df_merge_res_embalses_agregados.merge(df_aportes_agregados, how='left', left_on=['Fecha', 'RegionHidrologica'], right_on=['Fecha', 'RegionHidrologica'])

        # filling missing values
        df_merge_agregate['PromedioAcumuladoEnergia'].fillna(method='ffill', inplace=True)
        df_merge_agregate['MediaHistoricaEnergia'].fillna(method='bfill', inplace=True)

        # Create new columns for day, month, and year
        df_merge_agregate['Dia'] = df_merge_agregate['Fecha'].apply(lambda x: int(x.split('-')[2]))
        df_merge_agregate['Mes'] = df_merge_agregate['Fecha'].apply(lambda x: int(x.split('-')[1]))
        df_merge_agregate['Año'] = df_merge_agregate['Fecha'].apply(lambda x: int(x.split('-')[0]))
        df_merge_agregate.drop(columns=['Fecha','RegionHidrologica'], inplace=True)

        return df_merge_agregate
    
    def save_data_not_agregate(self, stale:bool)->None:
        """
        Save non-aggregated data to an Excel file.

        Args:
        - stale (bool): Flag indicating whether to save standardized or not standardized data.

        Returns:
        None
        """
        if stale:
            df_normalized = self._merge_data_not_agregate()
            df_normalized[['VolumenUtilDiarioEnergia', 'CapacidadUtilEnergia', 'VolumenTotalEnergia', 'VertimientosEnergia', 'SST', 'ANOM']] = self.scaler.fit_transform(df_normalized[['VolumenUtilDiarioEnergia', 'CapacidadUtilEnergia', 'VolumenTotalEnergia', 'VertimientosEnergia', 'SST', 'ANOM']])
            df_normalized.to_excel('Data/Results/Standardized/EmbalsesNoAgregados.xlsx', index=False)
        else:
            self._merge_data_not_agregate().to_excel('Data/Results/NotStandardized/EmbalsesNoAgregados.xlsx', index=False)
    
    def save_data_agregate(self,stale:bool)->None:
            """
            Save aggregated data to an Excel file, optionally applying data normalization.

            Parameters:
            - stale (bool): Flag indicating whether to apply data normalization.

            Returns:
            - None
            """
            if stale:
                df_normalized = self._merge_data_agregate()
                df_normalized[['VolumenUtilDiarioEnergia', 'CapacidadUtilEnergia', 'VolumenTotalEnergia', 'VertimientosEnergia', 'SST', 'ANOM','AportesHidricosEnergia','PromedioAcumuladoEnergia','MediaHistoricaEnergia']] = self.scaler.fit_transform(df_normalized[['VolumenUtilDiarioEnergia', 'CapacidadUtilEnergia', 'VolumenTotalEnergia', 'VertimientosEnergia', 'SST', 'ANOM','AportesHidricosEnergia','PromedioAcumuladoEnergia','MediaHistoricaEnergia']])
                df_normalized.to_excel('Data/Results/Standardized/EmbalsesAgregados.xlsx', index=False)
            else:
                self._merge_data_agregate().to_excel('Data/Results/NotStandardized/EmbalsesAgregados.xlsx', index=False)
            
if __name__ == "__main__":
    join_data = JoinData()
    df_paratec, df_simem_embalses, df_oni, df_simem_reservas, df_simem_aportes = join_data._clean_data()
    join_data.save_data_not_agregate(stale=True)
    join_data.save_data_agregate(stale=True)




