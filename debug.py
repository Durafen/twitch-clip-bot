import logging
import inspect
import utility
import config
import sys
import ntpath

if config.DEBUG:
    logging.basicConfig(filename='twitch-clip-bot.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)


def output_error(err):
    if config.DEBUG:
        logger.error(err)
        utility.print_usertoscreen("system", "bot", "Error: " + err)
#        utility.print_toscreen(err)


def output_debug(data):
    if config.DEBUG:
        logger.debug(data)
        utility.print_usertoscreen("system", "bot", "Debug: " + data)

#        utility.print_toscreen(data)

def lineno():
    cf = sys._getframe().f_back
    filename = path_leaf(inspect.getframeinfo(cf).filename)
    lineno = str(cf.f_lineno)
    return str(" " + filename + " line " + lineno)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
