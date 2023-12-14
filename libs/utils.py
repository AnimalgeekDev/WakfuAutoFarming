class Utils:
    def is_float(self, cadena):
        try:
            float(cadena)
            return True
        except:
            return False
    
    def is_int(self, cadena):
        try:
            int(float(cadena) // 1)
            return True
        except:
            return False