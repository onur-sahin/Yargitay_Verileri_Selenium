
import copy
from asyncio import Event
from distutils.util import convert_path
import signal
from threading import Thread
import time
import winsound

from my_tools import convert_all_lowercase, convert_all_uppercase, convert_title
cumle = " iıİI ahmed	vel ve ayşem <br>"
kelime = [i for i in " iıİI ahmed	vel ve ayşem <br>"]

cumle = convert_title(cumle)



print(cumle)


