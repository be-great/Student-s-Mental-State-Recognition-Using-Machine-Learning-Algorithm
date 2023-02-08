class Config(object): 
    pass 
 
class ProdConfig(Config): 
    pass 
 
class DevConfig(Config): 
    DEBUG = True
    UPLOAD_FOLDER = '/home/tasky/Documents/research_9/code/Steps/7-interface/myversion/UPLOAD_FOLDER/'
    SECRET_KEY="dflsdkfpsod923109@##"
    DATASET_PATH='/home/tasky/Documents/s10/research_9/code/Steps/7-interface/myversion/version2/dataset/'