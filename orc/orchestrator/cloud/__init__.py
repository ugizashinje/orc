from .amazon import AmazonCloudService

aws = AmazonCloudService()

def __getattr__(name):

    def call_method(*args, **kwargs):
        method = getattr(aws, name)
        return method(*args, **kwargs)

    return call_method