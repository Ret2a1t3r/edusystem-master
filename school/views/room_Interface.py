from abc import ABC, abstractmethod


class IShowRoomInfoService(ABC):
    @abstractmethod
    def show_room_info(self):
        pass


class IAddRoomService(ABC):
    @abstractmethod
    def room_add(self):
        pass


class IDeleteRoomService(ABC):
    @abstractmethod
    def room_delete(self):
        pass


class IEditRoomService(ABC):
    @abstractmethod
    def room_edit(self, room_id):
        pass
