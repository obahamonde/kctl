"""Utility functions for the Kubernetes module"""

import socket
import random
from uuid import uuid4
from datetime import datetime
from requests import get
from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from kubernetes.config import process


HOST: str = process.env.DOCKER_HOST
console = Console()
log = console.log

def get_name() -> str:
    return "".join(
        [
            random.choice("bcdfghjklmnpqrstvwxyz") + random.choice("aeiou")
            for i in range(random.randint(3, 5))
        ]
    ).capitalize()


def get_password() -> str:
    return "".join(
        [
            random.choice("bcdfghjklmnpqrstvwxyz0123456789")
            for i in range(random.randint(8, 12))
        ]
    )


def get_id() -> str:
    return str(uuid4())


def get_time() -> str:
    return datetime.now().isoformat()


def get_port() -> int:
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(("", 0))
    port = socket_server.getsockname()[1]
    socket_server.close()
    return port


def get_host() -> str:
    return HOST


def tstamp(ts: int) -> float:

    """Converts FaunaDB timestamp to Python timestamp"""

    return float(str(ts)[:10]+'.'+str(ts)[10:])

def uid() -> str:

    """Generates a random id"""

    return str(uuid4())


def avatar()->str:

    """Generates a random avatar"""

    return f"https://avatars.dicebear.com/api/avataaars/{uid()}.svg"


def now()->float:

    """Returns the current timestamp"""

    return datetime.now().timestamp()

