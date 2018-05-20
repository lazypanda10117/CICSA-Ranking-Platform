from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=200);
    event_description = models.CharField(max_length=50);
    event_status = models.CharField(max_length=50);
    event_type = models.CharField(max_length=50);
    event_host = models.CharField(max_length=50);
    event_location = models.CharField(max_length=50);
    event_region = models.CharField(max_length=50);
    event_boat_number = models.CharField(max_length=50);
    event_rotation_detail = models.CharField(max_length=50); #(team id: [rotation sequence], for each team)
    event_start_date = models.EmailField(max_length=200);
    event_end_date = models.CharField(max_length=200);
    event_teams = models.CharField(max_length=50); #(team id, tag) tuple
    event_races = models.CharField(max_length=50); #(tag, race ids) nested json
    event_summary = models.CharField(max_length=50); #id to summary
    event_create_time = models.DateTimeField('Creation Date');
    def __str__(self):
        return self;

class Region(models.Model):
    region_name = models.CharField(max_length=200);
    def __str__(self):
        return self;

class Season(models.Model):
    season_name = models.CharField(max_length=200);
    def __str__(self):
        return self;

class EventType(models.Model):
    event_type_name = models.CharField(max_length=200);
    def __str__(self):
        return self;

class EventActivity(models.Model):
    event_activity_type = models.CharField(max_length=200); #i.e. races
    event_activity_name = models.EmailField(max_length=200); #i.e. 1, 2, ...
    event_activity_result = models.CharField(max_length=200); #json
    event_activity_note = models.CharField(max_length=50);
    def __str__(self):
        return self;

class Summary(models.Model):
    summary_result = models.CharField(max_length=200); #json with team, gen-ranking, override ranking
    summary_score = models.EmailField(max_length=200); #json of autogen score for each team/school
    def __str__(self):
        return self;


class Log(models.Model):
    log_creator = models.IntegerField(); #if sql, then system, else user id
    log_content = models.IntegerField();
    log_type = models.IntegerField(); #i.e. user, sql
    log_create_time = models.DateTimeField('Comment Date');
    def __str__(self):
        return self;

class School(models.Model):
    school_name = models.IntegerField();
    school_region = models.IntegerField();
    school_status = models.IntegerField();
    school_season_score = models.IntegerField();
    school_season_race = models.IntegerField();
    def __str__(self):
        return self;

class Team(models.Model):
    team_name = models.IntegerField();
    team_school = models.IntegerField();
    team_status = models.IntegerField();
    def __str__(self):
        return self;

class MemberGroup(models.Model):
    member_id = models.IntegerField();
    def __str__(self):
        return self;

class Member(models.Model):
    member_name = models.IntegerField();
    member_school = models.IntegerField();
    member_email = models.IntegerField();
    member_status = models.IntegerField();
    def __str__(self):
        return self;

class Account(models.Model):
    account_type = models.IntegerField(); #school, admin
    account_email = models.IntegerField();
    account_salt = models.IntegerField();
    account_password = models.IntegerField();
    account_status = models.IntegerField();
    def __str__(self):
        return self;