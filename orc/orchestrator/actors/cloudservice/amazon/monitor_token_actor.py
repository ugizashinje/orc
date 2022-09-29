from orchestrator.automation.core import Handle, Step
import monitor_token_message


@Handle(monitor_token_message.MonitorTokenMessage)
class MonitorTokenActor:

    def starts_with(self):
        return self.check_tokens

    @Step()
    def check_tokens(self):
        print('MonitorTokenActor')