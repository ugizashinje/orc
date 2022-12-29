import orchestrator.cloud.amazon
from orchestrator.models import *
from orchestrator.automation.core import Delay
from orchestrator.actors.server.amazon.provision_server_message import ProvisionServerMessage

def name_gen():
    i = 0
    while True:
        i += 1
        yield f'server-{i}'

name = name_gen()

server = Server.objects.get(id=2)
def send():
    msg = ProvisionServerMessage()
    msg.name = next(name)
    orchestrator.cloud.amazon.send_request(msg, server, delay=Delay.NONE)
