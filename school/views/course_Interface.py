from abc import ABC, abstractmethod


class IShowCourseInfoService(ABC):
    @abstractmethod
    def show_course_info(self):
        pass


class IAddCourseService(ABC):
    @abstractmethod
    def course_add(self):
        pass


class IDeleteCourseService(ABC):
    @abstractmethod
    def course_delete(self):
        pass


class IArrangingCourseService(ABC):
    @abstractmethod
    def arranging_course(self):
        pass


class ISelectCourseService(ABC):
    @abstractmethod
    def select_course(self):
        pass


class IShowTeachTimeTableService(ABC):
    @abstractmethod
    def show_teach_time_table(self):
        pass


class IShowPreviousTeachingCourseInfoService(ABC):
    @abstractmethod
    def show_previous_teaching_course_info(self):
        pass


class IRecordScoreService(ABC):
    @abstractmethod
    def score_record(self, tp_id):
        pass


class IShowStuTimeTableService(ABC):
    @abstractmethod
    def show_stu_time_table(self):
        pass
