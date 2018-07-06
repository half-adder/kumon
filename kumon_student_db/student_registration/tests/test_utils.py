from datetime import date
from kumon_student_db.student_registration import utils
import calendar


def test_len_longest_ith_item_basic():
    items = [("1", "1"), ("22", "2"), ("333", "3")]
    assert utils.len_longest_ith_item(items, 0) == 3


def test_len_longest_ith_item_with_other_idx_longer():
    items = [("1", "1"), ("22", "2"), ("333", "4444")]
    assert utils.len_longest_ith_item(items, 0) == 3


# Calendar-related tests
def test_n_tuesdays_left_in_month_on_a_non_tuesday():
    d = date(2018, 7, 1)  # A Sunday in July, 2018
    assert utils.tuesdays_left(d) == 5


def test_n_tuesdays_left_on_a_tuesday_includes_that_tuesday():
    d = date(2018, 7, 3)  # A Tuesday in July, 2018
    assert utils.tuesdays_left(d) == 5


def test_n_tuesdays_left_on_last_tuesday_of_month_is_one():
    d = date(2018, 6, 26)  # The last Tuesday of June, 2018
    assert utils.tuesdays_left(d) == 1


def test_n_saturdays_left_in_month_on_a_non_saturday():
    d = date(2018, 7, 6)  # A Friday in July, 2018
    assert utils.saturdays_left(d) == 4


def test_n_saturdays_left_on_a_saturday_doesnt_include_that_saturday():
    d = date(2018, 7, 7)  # A Saturday in July, 2018
    assert utils.saturdays_left(d) == 4


def test_n_saturdays_left_on_last_saturday_of_month_is_zero():
    d = date(2018, 7, 28)  # The last Saturday of July, 2018
    assert utils.saturdays_left(d) == 1


def test_weekdays_in_month_has_correct_number_days_in_month():
    for year in range(1995, 2100):
        for month in range(1, 13):
            days_in_month = calendar.monthrange(year, month)[1]
            assert len(utils.sane_monthdays(year, month)) == days_in_month


def test_weekdays_in_month_starts_with_1():
    assert min([item[0] for item in utils.sane_monthdays(2018, 7)]) == 1


def test_n_weekdays_in_month():
    for weekday, n_weekdays_in_2018_7 in [
        (calendar.MONDAY, 5),
        (calendar.TUESDAY, 5),
        (calendar.WEDNESDAY, 4),
        (calendar.THURSDAY, 4),
        (calendar.FRIDAY, 4),
        (calendar.SATURDAY, 4),
        (calendar.SUNDAY, 5),
    ]:
        assert utils.n_weekdays_in_month(2018, 7, weekday) == n_weekdays_in_2018_7


def test_prorated_cost_ex1():
    start_date = date(2017, 11, 11)
    monthly_cost = 115
    assert 86 == utils.prorated_cost(start_date, monthly_cost)


def test_prorated_cost_ex2():
    start_date = date(2017, 12, 12)
    monthly_cost = 115
    assert 77 == utils.prorated_cost(start_date, monthly_cost)


def test_prorated_cost_ex3():
    start_date = date(2017, 11, 28)
    monthly_cost = 115
    assert 14 == utils.prorated_cost(start_date, monthly_cost)


def test_prorated_cost_ex4():
    start_date = date(2017, 10, 7)
    monthly_cost = 115
    assert 102 == utils.prorated_cost(start_date, monthly_cost)


