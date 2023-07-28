from flask_login import UserMixin
from ReadWeld.models import Welder, Worker
from ReadWeld import login_manager


class MasterLogin(UserMixin):
    
    def fromDB(self, worker_id):
        self.__worker = Worker.query.get(worker_id)
        return self

    def creat(self, worker: Worker):
        self.__worker = worker
        return self
    
    def get_id(self):
        return str(self.__worker.id)