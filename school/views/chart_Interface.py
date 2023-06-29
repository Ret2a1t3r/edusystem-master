from abc import ABC, abstractmethod


class IManagerAnalysisAchievementService(ABC):
    @abstractmethod
    def manager_analysis_achievement(self):
        pass


class ITeachAnalysisAchievementService(ABC):
    @abstractmethod
    def teach_analysis_achievement(self):
        pass


class IShowAnalysisInfo(ABC):
    @abstractmethod
    def show_analysis_info(self):
        pass
