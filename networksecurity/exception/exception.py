import sys
from networksecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return "Error occured in python script [{0}] in linenumber [{1}] error message [{2}] ".format(
            self.filename,
            self.lineno,
            self.error_message
        )
        
if __name__ =="__main__":
    try:
        logging.info("Entered into try block")
        a=10
        b=a/0
        print(b)
    except Exception as e:
        raise NetworkSecurityException(e,sys)