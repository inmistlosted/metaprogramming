from Settings.BlackLines.maximumblacklinessettings import MaximumBlackLinesSettings
from Settings.BlackLines.minimumblacklinessettings import MinimumBlackLinesSettings


class BlackLinesSettings(object):
    def __init__(self, settings):
        self.__minimumBlackLinesSettings = MinimumBlackLinesSettings(settings["MinimumBlackLines"])
        self.__maximumBlackLinesSettings = MaximumBlackLinesSettings(settings["KeepMaximumBlackLines"])

    def MinimumBlackLinesSettings(self):
        return self.__minimumBlackLinesSettings

    def MaximumBlackLinesSettings(self):
        return self.__maximumBlackLinesSettings
