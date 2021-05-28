import logging

from pyclier_demo.utils import demo_func
from pyclier import Command

log = logging.getLogger(__name__)

cmd = Command("add", func=demo_func)
cmd.add("-t", metavar="<branch>")
cmd.add("-m", metavar="<master>")
cmd.add("-f", action="store_true")
cmd.add("name", metavar="<name>")
cmd.add("url", metavar="<url>")
