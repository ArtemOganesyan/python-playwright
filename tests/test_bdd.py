from pytest_bdd import scenarios

from bdd.steps.bdd_steps import *  # noqa: F401,F403


scenarios("../bdd/features/bdd.feature")
