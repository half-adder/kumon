from kumon_student_db.student_registration import utils


def test_len_longest_ith_item_basic():
    items = [('1', '1'), ('22', '2'), ('333', '3')]
    assert utils.len_longest_ith_item(items, 0) == 3


def test_len_longest_ith_item_with_other_idx_longer():
    items = [('1', '1'), ('22', '2'), ('333', '4444')]
    assert utils.len_longest_ith_item(items, 0) == 3

