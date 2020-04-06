from gevent import monkey

monkey.patch_all()

from . import create_app  # noqa: E402 F401
