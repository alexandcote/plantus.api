from plantus.celery import app


@app.task(bind=True)
def sensor_analyser():
    """
    Task that analyse each pot of the database and create operation
    """
    # TODO: Discuss how we do this...
    print("Analyse ...")
