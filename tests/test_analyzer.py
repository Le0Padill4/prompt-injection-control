import pytest

from csv_processor import read_records, total_amount


def test_read_and_sum(tmp_path):
    source = tmp_path / "orders.csv"
    source.write_text("item,amount\nbook,10.5\npen,2\n", encoding="utf-8")
    records = read_records(source)
    assert len(records) == 2
    assert total_amount(records) == pytest.approx(12.5)


@pytest.mark.xfail(reason="Known validation gap: non-numeric amount is not handled")
def test_invalid_amount_has_clear_error(tmp_path):
    source = tmp_path / "orders.csv"
    source.write_text("item,amount\nbook,not-a-number\n", encoding="utf-8")
    with pytest.raises(ValueError, match="amount"):
        total_amount(read_records(source))
