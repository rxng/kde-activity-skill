from mycroft import MycroftSkill, intent_file_handler


class KdeActivity(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('activity.kde.intent')
    def handle_activity_kde(self, message):
        self.speak_dialog('activity.kde')


def create_skill():
    return KdeActivity()

