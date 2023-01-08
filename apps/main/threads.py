import threading
import os


class CreateDeployAppThread(threading.Thread):
    def __init__(self, domain, app_id):
        super(CreateDeployAppThread, self).__init__()
        self.domain = domain
        self.app_id = app_id

    def run(self):
        try:
            print(f"[+] Starting deployment for domain: {self.domain} app: {self.app_id}")
            # os.system(f'/home/khaled/landing_pages/landing-pages-generator/venv/bin/ansible-playbook --extra-vars="domain={self.domain}" --extra-vars="app_id={self.app_id}" /home/khaled/landing_pages/ansible-landing-generator/deploy.yml')
        except Exception as e:
            print(e)
