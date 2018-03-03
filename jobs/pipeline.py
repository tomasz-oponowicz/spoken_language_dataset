class Pipeline:
    def __init__(self, jobs, context=None):
        self.jobs = jobs
        self.context = context or {}

    def execute(self):
        for job in self.jobs:
            job.execute(self.context)
