from abc import ABC, abstractmethod


class IShowTeachInfoService(ABC):
    @abstractmethod
    def show_teach_info(self):
        pass


class IAddTeachService(ABC):
    @abstractmethod
    def teach_add(self):
        pass


class IDeleteTeachService(ABC):
    @abstractmethod
    def teach_delete(self):
        pass


class IEditTeachService(ABC):
    @abstractmethod
    def teach_edit(self, teach_id):
        pass


