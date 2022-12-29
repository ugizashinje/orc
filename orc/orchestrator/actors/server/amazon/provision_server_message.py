class ProvisionServerMessage:
    def __init__(self, instance_type='t4g.micro'):
        self.instance_type = instance_type
        self.name = None