from generators import gen_static
from base_config import config

class Engine:
    """This is the engine that is builds your static site. 
    
    Use Engine.run() to output the files to the designated output path."""
    
    config = config['DEFAULT']
    
    def __init__(self, *, conent_path, output_path):
        self.conent_path = content_path
        self.output_path = output_path
        
    def build(self):
        pass
        
    def run(self, overwrite=True):
    return gen_static(static_path=STATIC_PATH, overwrite=overwrite)
