''' upgrade to 1001 '''


def run_upgrade(setup_context):
    """ un upgrade to 1001
    """

    setup_context.runImportStepFromProfile(
        "profile-eea.restapi:default",
        "catalog",
        run_dependencies=False,
        purge_old=False,
    )
