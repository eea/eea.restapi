def run_upgrade(setup_context):
    """
    """

    setup_context.runImportStepFromProfile(
        "profile-eea.restapi:default",
        "catalog",
        run_dependencies=False,
        purge_old=False,
    )
