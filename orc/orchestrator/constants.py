class Server:
    class Status:
        PENDING = "pending"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        STOPPED = "stopped"
        TERMINATING = "terminating"
        TERMINATED = "terminated"

        ADMIN_CHOICES = [
            (PENDING, PENDING),
            (STARTING, STARTING),
            (RUNNING, RUNNING),
            (STOPPING, STOPPING),
            (STOPPED, STOPPED),
            (TERMINATING, TERMINATING),
            (TERMINATED, TERMINATED)
        ]

