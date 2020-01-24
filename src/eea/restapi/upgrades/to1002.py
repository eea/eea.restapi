def run_upgrade(setup_context):
    """
    """

    setup_context.runImportStepFromProfile(
        "profile-eea.restapi:upgrade_1002",
        "typeinfo",
        run_dependencies=False,
        purge_old=False,
    )
