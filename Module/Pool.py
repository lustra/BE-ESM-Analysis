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


def fun(f,q_in,q_out):
    while True:
        i,x = q_in.get()
        if i is None:
            break
        q_out.put((i,f(x)))


def parmap(f, n, nprocs=cpu_count()):
    q_in = Queue(1)
    q_out = Queue()

    proc = [Process(target=fun,args=(f, q_in, q_out)) for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(n)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]
