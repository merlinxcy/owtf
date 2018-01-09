"""
owtf.lib.owtf_process
~~~~~~~~~~~~~~~~~~~~~

Consists of owtf process class and its manager
"""

import logging
from multiprocessing import Process, Queue
import multiprocessing
import sys

from owtf.db.database import Session, get_db_engine
from owtf.utils.file import get_log_path
from owtf.utils.formatters import FileFormatter, ConsoleFormatter


class OWTFProcess(Process):
    """
    Implementing own proxy of Process for better control of processes launched
    from OWTF both while creating and terminating the processes
    """

    def __init__(self, **kwargs):
        """
        Ideally not to override this but can be done if needed. If overridden
        please give a call to super() and make sure you run this
        """
        self.poison_q = Queue()
        self._process = None
        self.output_q = None
        Session.configure(bind=get_db_engine())
        self.session = Session()
        for key in list(kwargs.keys()):  # Attach all kwargs to self
            setattr(self, key, kwargs.get(key, None))
        super(OWTFProcess, self).__init__()

    def initialize(self, **kwargs):
        """
        Supposed to be overridden if user wants to initialize something
        """
        pass

    def run(self):
        """This method must not be overridden by user

        Sets proper logger with file handler and Formatter
        and launches process specific code

        :return: None
        :rtype: None
        """
        try:
            self.pseudo_run()
        except KeyboardInterrupt:
            # In case of interrupt while listing plugins
            pass

    def pseudo_run(self):
        """
        This method must be overridden by user with the process related code
        """
        pass