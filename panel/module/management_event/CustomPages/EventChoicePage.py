from django.urls import reverse

from panel.module.base.block.CustomPages import AbstractBasePage


class EventChoicePage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_event/event.html'

    def genPageObject(self):
        contents = [
            dict(
                event_type='Fleet Race',
                description='View all the fleet race event related entries here',
                button_description='View Fleet Races',
                destination=reverse(
                    'panel.module.management_event.view_dispatch_param',
                    args=['event', 'fleet race']
                ),
            ),
            dict(
                event_type='Team Race (Work in Progress)',
                description='Still a work in progress',
                button_description='View Team Races',
                destination='#',
            ),
        ]
        return dict(block_title='Event Types', contents=contents)

    def render(self):
        return super().renderHelper(self.genPageObject())

    def parseParams(self, param):
        return None
