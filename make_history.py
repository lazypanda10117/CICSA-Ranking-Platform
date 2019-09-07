# After running this, there will be a new season created
# OR, we pass to this function the current season and the new season
def make_history(current_season, new_season):
    # For each HasHistoryModel model:
        # Query each object from the current season
        # For each object
            # Make a copy of it
            # Set the season to the new season
    # Fix foreign keys for all new objects

    current_season = ConfigAPI(self.request).getSeason()
    new_season = ???
    # Region, ScoreMapping, School, MemberGroup, Member
    has_history_models_querysets = [
        Region.objects.all(),
        ScoreMapping.objects.all(),
        School.objects.all(),
        MemberGroup.objects.all(),
        Member.objects.all()
    ]

    # Make copies of the current_season objects

    for models_queryset in has_history_models_querysets:
        current_season_queryset = models_queryset.filter(season=current_season)
        for obj in current_season_queryset:
            # If universal_id isn't set, set it to the id
            if obj.universal_id is None:
                obj.universal_id = obj.id
                obj.save()
            obj.pk = None
            obj.id = None
            obj.save() # Makes copy because pk, id is None
            obj.season = new_season
            obj.save()

    # Fix foreign keys

    # School has a Region fk school_region
    new_schools = School.objects.filter(season=new_season)
    for school in new_schools:
        old_region = Region.objects.get(id=school.school_region)
        new_region = Region.objects.get(season=new_season, universal_id=old_region.universal_id)
        school.school_region = new_region.id
        school.save()

    # MemberGroup has a School fk member_group_school
    # MemberGroup has Member m2m member_group_member_ids
    new_member_groups = MemberGroup.objects.filter(season=new_season)
    for member_group in new_member_groups:
        old_school = School.objects.get(id=member_group.member_group_school)
        new_school = School.objects.get(season=new_season, universal_id=old_school.universal_id)
        member_group.member_group_school = new_school.id

        old_member_ids = member_group.member_group_member_ids
        new_member_ids = []
        for member_id in old_member_ids:
            old_member = Member.objects.get(id=member_id)
            new_member = Member.objects.get(season=new_season, universal_id=old_member.universal_id)
            new_member_ids.append(new_member.id)
        member_group.member_group_member_ids = new_member_ids
        member_group.save()

    # Member has a School fk member_school
    new_members = Member.objects.filter(season=new_season)
    for member in new_members:
        old_school = School.objects.get(id=member.member_school)
        new_school = School.objects.get(season=new_season, universal_id=old_school.universal_id)
        member.member_school = new_school.id
        member.save()