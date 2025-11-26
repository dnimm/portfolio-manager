from portfolioapp.cli import constants

def test_constants_values_exist():
    assert constants.LOGIN_MENU == 0
    assert constants.MAIN_MENU == 1
    assert constants.MANAGE_USERS_MENU == 2
    assert constants.MANAGE_PORTFOLIOS_MENU == 3
    assert constants.MARKETPLACE_MENU == 4
