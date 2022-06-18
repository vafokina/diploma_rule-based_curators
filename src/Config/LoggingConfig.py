import logging

def getLogger(name = None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
 
    h = logging.StreamHandler()
    fmt = '%(asctime)s - %(levelname)s - [%(threadName)s] %(name)s : %(message)s'
    formatter = logging.Formatter(fmt)
    h.setFormatter(formatter)
 
    logger.addHandler(h)
    logger.propagate = False
    return logger

def getCuratorEngineLogger(name = None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fmt = '%(asctime)s - %(levelname)s - %(name)s : %(message)s'
    formatter = logging.Formatter(fmt)
 
    mainHandler = logging.StreamHandler()
    mainHandler.setFormatter(formatter)

    #streamer = StringIO()
    #streamHandler = logging.StreamHandler(stream=streamer)
    #streamHandler.setFormatter(formatter)
    #streamHandler.setLevel(logging.INFO)
    
    logger.addHandler(mainHandler)
    #logger.addHandler(streamHandler)
    logger.propagate = False
    return logger

