import calendar


def flatten(l):
    """Flatten a list of lists"""
    return [item for sublist in l for item in sublist]


def len_longest_ith_item(items, i):
    """Return the length of the longest ith item in the list of tuples"""
    return max(map(lambda tup: len(tup[i]), items))


def sane_monthdays(year, month):
    """
    Returns an list containing (month_day, weekday) of the given month, where month_day
    ranges from [1,31] and weekday ranges from [0,6] and 0==Monday, 6==Sunday

    The python stdlib supplies a function that is nearly identical, but they pad the
    range to include full weeks at the beginning and end. This function is a simple
    wrapper, but includes ONLY dates inside the supplied month.
    """
    c = calendar.Calendar(calendar.MONDAY)
    return [
        (cal_date.day, cal_date.weekday())  # assumes that the first day is Monday
        for cal_date in c.itermonthdates(year, month)
        if cal_date.month == month
    ]


def tuesdays_left(d):
    """Return number of Tuesdays left in the given date's month INCLUDING the given date"""
    return weekdays_left(d, calendar.TUESDAY)


def saturdays_left(d):
    """Returns number of Saturdays left in the given date's month INCLUDING the given date"""
    return weekdays_left(d, calendar.SATURDAY)


def weekdays_left(d, weekday):
    """
    Returns the number of the given weekdays left in the given date's month INCLUDING the
    given date.

    Weekdays range from 0 (Monday) to 6 (Sunday). A convenient mapping can be found in
    the calendar module in the stdlib (calendar.MONDAY, etc).
    """
    n_weekdays_left = 0
    for month_day, week_day in sane_monthdays(d.year, d.month):
        if month_day >= d.day and week_day == weekday:
            n_weekdays_left += 1
    return n_weekdays_left


def n_weekdays_in_month(year, month, weekday):
    """
    Returns the total number of the given weekdays in the given year and month

    Weekdays range from 0 (Monday) to 6 (Sunday). A convenient mapping can be found in
    the calendar module in the stdlib (calendar.MONDAY, etc).
    """
    n_weekdays_left = 0
    for _, cal_weekday in sane_monthdays(year, month):
        if cal_weekday == weekday:
            n_weekdays_left += 1
    return n_weekdays_left


def prorated_cost(start_date, monthly_cost):
    """Return the prorated cost given the start_date and monthly_cost"""
    class_days_left = 0
    total_class_days = 0

    class_days_left += tuesdays_left(start_date) + saturdays_left(start_date)

    total_class_days += n_weekdays_in_month(
        start_date.year, start_date.month, calendar.SATURDAY
    ) + n_weekdays_in_month(start_date.year, start_date.month, calendar.TUESDAY)

    return round((class_days_left / total_class_days) * monthly_cost)


def total_cost(start_date, monthly_cost, registration_cost, n_subjects):
    per_subj_cost = prorated_cost(start_date, monthly_cost) + (2 * monthly_cost)
    return registration_cost + (n_subjects * per_subj_cost)
