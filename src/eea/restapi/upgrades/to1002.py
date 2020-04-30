''' upgrade to 1002 '''


def run_upgrade(setup_context):
    """ run upgrade to 1002
    """

    setup_context.runImportStepFromProfile(
        "profile-eea.restapi:upgrade_1002",
        "typeinfo",
        run_dependencies=False,
        purge_old=False,
    )
