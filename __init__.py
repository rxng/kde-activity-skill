import sys
import pydbus
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler


class KdeActivity(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(KdeActivity, self).__init__(name="KdeActivity")
        # Initialize working variables used within the skill.
        self.user = ""  # change this to your default desktop user
        self.activity = ""
        bus = pydbus.SessionBus()
        self._activity_bus = bus.get(
            "org.kde.ActivityManager", "/ActivityManager/Activities"
        )


    def _find_id(self, name):
        for activity_id in self._activity_bus.ListActivities(
            2
        ) + self._activity_bus.ListActivities(4):
            if name.casefold() == self._activity_bus.ActivityName(activity_id).casefold():
                return activity_id
        raise ValueError("No activity exist with the name: {}".format(name))

    @intent_handler(IntentBuilder("").require("ActivityStart").build())
    def handle_activitylauncher_open_intent(self, message):
        try:
            cmd = message.data.get('ActivityStart')
            msg = message.data.get('utterance')
            self.activity = str(msg).replace(cmd+" ", "", 1)

            if len(self.activity) != 36:
                self.id = self._find_id(self.activity)
            else:
                self.id = self.activity

            bus = pydbus.SessionBus()

            remote_object = self._activity_bus

            remote_object.StartActivity(
                self.id)

            self.speak_dialog("activity.open", data={"activity": self.activity})

        except Exception as e:
            self.speak_dialog("activity.error")

    @intent_handler(IntentBuilder("").require("ActivityStop").build())
    def handle_activitylauncher_close_intent(self, message):
        try:
            cmd = message.data.get('ActivityStop')
            msg = message.data.get('utterance')
            self.activity = str(msg).replace(cmd+" ", "", 1)

            if len(self.activity) != 36:
                self.id = self._find_id(self.activity)
            else:
                self.id = self.activity

            bus = pydbus.SessionBus()

            remote_object = self._activity_bus

            remote_object.StopActivity(
                self.id)

            self.speak_dialog("activity.close", data={"activity": self.activity})

        except Exception as e:
            self.speak_dialog("activity.error")


def create_skill():
    return KdeActivity()

