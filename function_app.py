import azure.functions as func
from pydataxm.pydatasimem import ReadSIMEM

file = ReadSIMEM('BA1C55', str('2013-05-01'), str('2025-05-01'))
data = file.main(filter=False)
data.to_excel('Data\SIMEM\AportesHidricos.xlsx',index=False)