from binaryninja import log

from .src.yan85 import Yan85

def init():
    log.log_debug("yan85 plugin loading")
    Yan85.register()
    log.log_info("yan85 plugin loaded successfully")
   
init()