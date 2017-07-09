#
# This file is part of the Awareness Operator Python implementation.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from abc import ABCMeta, abstractmethod
import threading
import logging
import socket
import ssl



class Backend(metaclass=ABCMeta):
    @abstractmethod
    def threading_async(self, function, args=(), kwargs={}, callback=None):
        raise NotImplementedError()

    @abstractmethod
    def processing_async(self, function, args=(), kwargs={}, callback=None):
        raise NotImplementedError()

    @abstractmethod
    def connect(self, host, port=1600):
        raise NotImplementedError()

    @abstractmethod
    def listen(self, host='', port=1600, use_ipv6=False, backlog=5):
        raise NotImplementedError()



class NativeBackend(Backend):


    def threading_async(self, function, args=(), kwargs={}, callback=None, daemon=True, name=None):
        if not callback:
            callback = lambda *args,**kwargs:None

        def wrap_with_callback(function, callback):
            returnvalue = lambda *args, **kwargs: callback(function(*args, **kwargs))
            return returnvalue

        thread = threading.Thread(target=wrap_with_callback(function, callback), args=args, kwargs=kwargs)
        thread.daemon = daemon
        if name:
            thread.name = name
        thread.start()

        return thread


    def processing_async(self, function, args=(), kwargs={}, callback=None, daemon=True, name=None):
        pass


    def connect(self, host, port=1600):

        sock = socket.create_connection((host, port))
        #sock = ssl.wrap_socket(sock)

        return sock


    def listen(self, host='', port=1600, use_ipv6=False, backlog=5):
        type = socket.AF_INET6 if use_ipv6 else socket.AF_INET

        listener = socket.socket(type, socket.SOCK_STREAM)
        #listener = ssl.wrap_socket(listener, server_side=True)

        listener.bind((host, port))
        listener.listen(backlog)

        return listener


    @classmethod
    def setup_logger(self):
        logger = logging.getLogger('awareness')
        logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(threadName)-20s | %(levelname)-8s | %(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)

        return logger
