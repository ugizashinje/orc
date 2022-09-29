import logging

from orchestrator.actors.server.amazon.provision_server_message import ProvisionServerMessage
from orchestrator.automation.core import Step, Handle, Actor, Delay


@Handle(ProvisionServerMessage)
class ProvisionServerActor(Actor):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def starts_with(self):
        return self.validate

    @Step()
    def validate(self):
        self.logger.debug('Amazon start server')

        return self.next(self.provision_server, Delay.NONE)

    @Step()
    def provision_server(self):
        return self.next(self.finish)
