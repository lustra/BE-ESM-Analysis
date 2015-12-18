# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from multiprocessing import *


def parallel(fkt, port):
    """
    :type fkt: ()->
    :type port: multiprocessing.queues.Queue
    """
    port.put(fkt(port.get()))


def omap(fkt, par):
    """
    :type fkt: ()->
    :type par: list
    :rtype: list
    """
    kerne = range(cpu_count())
    port = [None] * len(kerne)
    """ :type: list[multiprocessing.queues.Queue] """
    prozess = [None] * len(kerne)
    """ :type: list[Process] """
    for k in kerne:
        port[k] = Queue()
        prozess[k] = Process(target=parallel, args=(fkt, port[k]))

    for p in par:
        warte = True
        while warte:
            for k in kerne:
                if not prozess[k].is_alive():
                    port[k].put(p)
                    prozess[k].start()
                    warte = False
