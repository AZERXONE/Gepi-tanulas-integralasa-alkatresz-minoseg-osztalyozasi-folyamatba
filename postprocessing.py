import pandas as pd

class PostProcess:

    def __init__(self):

        self.check_list = {
            'AVARAGE_EXTRA_MATERIAL':   None,
            'MAX_EXTRA_MATERIAL':       None,
            'MAX_AREA_BETWEEN':         None,
            'MIN_AREA_BETWEEN':         None,
            'AVARAGE_AREA_BETWEEN':     None,
        }

    def check(self, df: pd.DataFrame) -> bool:

        validation_table = [
            self.avarageExtraMaterial,
            self.maxExtraMaterial,
            self.maxAreaBetween,
            self.minAreaBetween,
            self.avarageAreaBetween,
        ]

        with open('conf.ini', 'r', encoding='utf-8') as file:

            lines = file.readlines()[1:len(validation_table)+1]

        for idx, key in enumerate(self.check_list.keys()):
            
            if key == lines[idx].split(':')[0].strip():

                self.check_list[key] = str(lines[idx].split(':')[-1]).strip()
        
        for idx, value in enumerate(self.check_list.values()):
            
            if validation_table[idx](df,value) == True: return False
            
        return True
    
    def strToBool(self, value: str) -> bool:
        
        if value == "False": return False
        return True
            
    def avarageExtraMaterial(self, df: pd.DataFrame, condition: str) -> bool:
        
        if condition == "None": return False
        condition = float(condition)
        
        value = df['avarage_extra_material']
        if (value >= condition).any(): return True
        return False

    def maxExtraMaterial(self, df: pd.DataFrame, condition: str) -> bool:
        
        if condition == "None": return False
        condition = float(condition)
        
        value = df['max_extra_material']
        if (value >= condition).any(): return True
        return False

    def maxAreaBetween(self, df: pd.DataFrame, condition: str) -> bool:

        if condition == "None": return False
        condition = float(condition)

        value = df['max_area_between']
        if (value >= condition).any(): return True
        return False

    def minAreaBetween(self, df: pd.DataFrame, condition: str) -> bool:

        if condition == "None": return False
        condition = float(condition)

        value = df['min_area_between']
        if (value >= condition).any(): return True
        return False

    def avarageAreaBetween(self, df: pd.DataFrame, condition: str) -> bool:

        if condition == "None": return False
        condition = float(condition)

        value = df['avarage_area_between']
        if (value >= condition).any(): return True
        return False