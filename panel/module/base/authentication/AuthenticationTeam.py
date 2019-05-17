from misc.CustomElements import Dispatcher
from panel.config.team.management_data.CustomPages import *
from panel.config.team.management_data.CustomForms import *
from panel.module.ModuleRegistry import ModuleRegistry


class AuthenticationTeam:
    @staticmethod
    def getIdentifier():
        return 'team'

    @staticmethod
    def getAllowedModules():
        allowedModules = [
            ModuleRegistry.MANAGEMENT_DATA,
            ModuleRegistry.MANAGEMENT_EVENT,
            ModuleRegistry.MANAGEMENT_RANKING
        ]
        return allowedModules

    class ManagementData:
        @staticmethod
        def getTemplateBase():
            return 'platform/module/management_data/team_base.html'

        @staticmethod
        def getDataGeneralDispatcher():
            dispatcher = Dispatcher()
            dispatcher.add('season', {'class': Season, 'form': SeasonForm})
            dispatcher.add('region', {'class': Region, 'form': RegionForm})
            dispatcher.add('event type', {'class': EventType, 'form': EventTypeForm})
            dispatcher.add('score mapping', {'class': ScoreMapping, 'form': ScoreMappingForm})
            dispatcher.add('log', {'class': Log, 'form': LogForm})
            return dispatcher

        @staticmethod
        def getDataCustomDispatcher():
            dispatcher = Dispatcher()
            dispatcher.add('fleet race', {'class': FleetManagementView, 'form': EventManagementForm})
            dispatcher.add('team race', {'class': TeamManagementView, 'form': EventManagementForm})
            dispatcher.add('event', {'class': EventView, 'form': EventForm})
            dispatcher.add('summary', {'class': SummaryView, 'form': SummaryForm})
            dispatcher.add('event activity', {'class': EventActivityView, 'form': EventActivityForm})
            dispatcher.add('event tag', {'class': EventTagView, 'form': EventTagForm})
            dispatcher.add('event team', {'class': EventTeamView, 'form': EventTeamForm})
            dispatcher.add('school', {'class': SchoolView, 'form': SchoolForm})
            dispatcher.add('team', {'class': TeamView, 'form': TeamForm})
            dispatcher.add('member', {'class': MemberView, 'form': MemberForm})
            dispatcher.add('member group', {'class': MemberGroupView, 'form': MemberGroupForm})
            dispatcher.add('account', {'class': AccountView, 'form': AccountForm})
            return dispatcher


