from cicsa_ranking.models import MemberGroup
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class MemberGroupAPI(GeneralModelAPI):
    def setBaseClass(self):
        return MemberGroup;

    def getMemberGroupName(self, member_group_id):
        if member_group_id is not None:
            member_group = self.auth_class.authenticate('view', gf.getModelObject(MemberGroup, id=member_group_id));
            member_group_name = member_group.member_group_name;
            return member_group_name;
        return 'Unlinked';

    def getMemberGroupLink(self, member_group_id):
        if member_group_id is not None:
            member_group = self.auth_class.authenticate('view', gf.getModifiyLink('member group', id=member_group_id));
            member_group_name = member_group.member_group_name;
            return member_group_name;
        return '#';