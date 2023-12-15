import traceback

def add_data(obj,db):
    try:
        db.add(obj)
        db.commit()
        return True
    except Exception as err:
        traceback.print_exc()
        return None