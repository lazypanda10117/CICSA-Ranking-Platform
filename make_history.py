# After running this, there will be a new season created
# OR, we pass to this function the current season and the new season
def make_history():
    # For each model, if it is a HasHistoryModel:
        # Query each object from the current season
        # For each object, make a copy of it and on the new copy, set the season to the new season
    # Fix foreign keys for all new objects