import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# função para configurar o logger
# name = nome do logger
# log_file = nome do arquivo log
def loggerSetup(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

#debugLogger = loggerSetup('debugar', 'testLog.txt', level=logging.DEBUG)
#infoLogger = loggerSetup('informar', 'testLog.txt', level=logging.INFO)

#debugLogger.debug('mensagem debug')
#infoLogger.info('mensagem info')