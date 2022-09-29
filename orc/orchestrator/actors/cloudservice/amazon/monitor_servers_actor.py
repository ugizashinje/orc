from orchestrator.automation.core import Handle, Step
import monitor_servers_message


@Handle(monitor_servers_message.MonitorServersMessage)
class MonitorServersActor:

    def starts_with(self):
        return self.validate

    @Step()
    def validate(self):
        print('validate')