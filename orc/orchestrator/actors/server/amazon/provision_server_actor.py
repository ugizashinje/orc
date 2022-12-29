import logging

from orchestrator.actors.server.amazon.provision_server_message import ProvisionServerMessage
from orchestrator.automation.core import Step, Handle, Actor, Delay


@Handle(ProvisionServerMessage)
class ProvisionServerActor(Actor):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def first_step(self):
        return self.validate

    @Step()
    def validate(self):
        self.logger.debug(f'Amazon validate server {self.input["name"]}')
        self.data['arg'] = 3
        return self.next(self.provision_server, Delay.ONE)

    @Step()
    def provision_server(self, arg=None):
        self.data["server"] = self.input["name"]
        self.logger.debug(f'Amazon provision server {self.input["name"]} , arg: {arg} ')

        return Actor.COMPLETED
