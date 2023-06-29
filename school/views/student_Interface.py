from abc import ABC, abstractmethod


class IShowStuInfoService(ABC):
    @abstractmethod
    def show_stu_info(self):
        pass


class IShowStuInClassInfoService(ABC):
    @abstractmethod
    def show_stu_in_class_info(self, tp_id):
        pass


class IShowStuInPreviousClassService(ABC):
    @abstractmethod
    def show_stu_in_previous_class_info(self, tp_id):
        pass


class IAddStudentService(ABC):
    @abstractmethod
    def stu_add(self):
        pass


class IDeleteStudentService(ABC):
    @abstractmethod
    def stu_delete(self):
        pass


class IEditStudentService(ABC):
    @abstractmethod
    def stu_edit(self, stu_id):
        pass


class IQueryGradeService(ABC):
    @abstractmethod
    def query_grade(self):
        pass


