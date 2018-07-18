INSERT INTO ranking_account (account_type, account_email, account_salt, account_password, account_status, account_linked_id) VALUES ('admin', 'test@sailingdinosaurs.com', 'ITBZB20GC3L4E7N', '6ccca03c25e0c679b3069937106fbf905be5cae157eaaa78922f48db', 'active',  -1);

INSERT INTO ranking_eventtype (event_type_name) VALUES ('fleet race');
INSERT INTO ranking_eventtype (event_type_name) VALUES ('team race');

INSERT INTO ranking_season (season_name) VALUES ('Fall 2017');
INSERT INTO ranking_season (season_name) VALUES ('Winter 2017');
INSERT INTO ranking_season (season_name) VALUES ('Spring 2018');
INSERT INTO ranking_season (season_name) VALUES ('Summer 2018');
INSERT INTO ranking_season (season_name) VALUES ('Fall 2018');

INSERT INTO ranking_region (region_name) VALUES ('British Columbia');
INSERT INTO ranking_region (region_name) VALUES ('Alberta');
INSERT INTO ranking_region (region_name) VALUES ('Manitoba');
INSERT INTO ranking_region (region_name) VALUES ('Saskathewan');
INSERT INTO ranking_region (region_name) VALUES ('Other East Territories');
INSERT INTO ranking_region (region_name) VALUES ('Ontario');
INSERT INTO ranking_region (region_name) VALUES ('Quebec');
INSERT INTO ranking_region (region_name) VALUES ('Maritime Provinces');

INSERT INTO ranking_scoremapping (score_name, score_value) VALUES ('OCF', -10);
INSERT INTO ranking_scoremapping (score_name, score_value) VALUES ('DNF', -10);
INSERT INTO ranking_scoremapping (score_name, score_value) VALUES ('DNS', -10);

INSERT INTO ranking_school (school_name, school_region, school_season_score, school_default_team_name) VALUES ('UBC', 1, 'active', 0, 'False Red');
INSERT INTO ranking_school (school_name, school_region, school_season_score, school_default_team_name) VALUES ('University of Waterloo', 1, 'active', 0, 'False Red');
INSERT INTO ranking_school (school_name, school_region, school_season_score, school_default_team_name) VALUES ('University of Toronto', 1, 'active', 0, 'False Red');
INSERT INTO ranking_school (school_name, school_region, school_season_score, school_default_team_name) VALUES ("Queen's University", 1, 'active', 0, 'False Red');

INSERT INTO ranking_account (account_type, account_email, account_salt, account_password, account_status, account_linked_id) VALUES ('school', 'ubc@ubc.com', '72JC5B3QMH5Y10B', 'f6f986e2af9270c32d1886444b0d8962bf437ce54150f67543bfa45f', 'active',  1);
INSERT INTO ranking_account (account_type, account_email, account_salt, account_password, account_status, account_linked_id) VALUES ('school', 'uw@uw.com', 'KL8A2KMHTCON50B', '1a3d4fe4cb716c05ceba1f9b0fb3f64582c0cad9333a3dab1b032a76', 'active',  2);
INSERT INTO ranking_account (account_type, account_email, account_salt, account_password, account_status, account_linked_id) VALUES ('school', 'uoft@uoft.com', '3EW0GKBZJJVHF0B', 'f9093813963d768fdf6c088e6729c0e39c4e19e52d538a9013cd4df7', 'active',  3);
INSERT INTO ranking_account (account_type, account_email, account_salt, account_password, account_status, account_linked_id) VALUES ('school', 'queens@queens.com', 'UHSPRK8QB7CORME', '1cadbff866ecad0257dc5fb5e0af87437b6c56c55640c1f956e4d84f', 'active',  4);