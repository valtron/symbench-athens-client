import jenkins

__all__ = ["SymbenchAthensClient"]


class SymbenchAthensClient:
    """The client to the symbench athens server.
    
    Parameters
    ----------
    jenkins_url: str
        The url for the jenkins server
    username: str
        The username to login with
    password: str
        The password to login with

    Attributes
    ----------
    server: jenkins.Jenkins
        The python interface for the jenkins server
    """
    def __init__(self, jenkins_url, username, password):
       self.server = jenkins.Jenkins(
           jenkins_url,
           username=username,
           password=password
       )
    

    def get_user_info(self):
        """Return information for the currently logged in user."""
        return self.server.get_whoami()

    def get_available_jobs(self, names_only=False):
        """Returns available jobs from the server.
        
        Parameters
        ----------
        names_only: bool, default=False
            If true, return the job names only
        
        Returns
        -------
        list of dict or list of str
            The jobs available in the server
        """
        jobs = self.server.get_all_jobs()
        return list(map(lambda x: x['fullname'], jobs)) if names_only else jobs

    def get_job_info(self, job_name):
        self.server.assert_job_exists(job_name)
        return self.server.get_job_info(job_name)

    def get_job_config(self, job_name):
        self.server.assert_job_exists(job_name)
        return self.server.get_job_config(job_name)