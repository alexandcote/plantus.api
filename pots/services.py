from plantus.tasks import task_to_water_pot


def service_to_water_pot(pot):
    """ 
    Task to water a pot 
    TODO: Add tests when the function is completed 
    """
    time = 5
    task_to_water_pot.delay(pot.id, time)
