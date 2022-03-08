import datetime
import logging

from bom.logger import formatter


def test_get_extra_fields() -> None:
    record = logging.LogRecord(
        name="a",
        level=logging.INFO,
        pathname="b",
        lineno=10,
        msg="c",
        args=None,
        exc_info=None,
    )
    record.first = "first"  # type: ignore
    record.second = False  # type: ignore
    record.third = {"a": "b"}  # type: ignore
    record.fourth = 1.123  # type: ignore
    record.fifth = 1  # type: ignore
    record.sixth = ["a", "b"]  # type: ignore
    record.seventh = None  # type: ignore
    record.eigth = object  # type: ignore
    fields = formatter.get_extra_fields(record)
    assert {
        "first": "first",
        "second": False,
        "third": {"a": "b"},
        "fourth": 1.123,
        "fifth": 1,
        "sixth": ["a", "b"],
        "seventh": None,
        "eigth": "<class 'object'>",
    } == fields


def test_json_formatter() -> None:
    json_formatter = formatter.JsonFormatter()
    record = logging.LogRecord(
        name="a",
        level=logging.INFO,
        pathname="b",
        lineno=10,
        msg="c",
        args=None,
        exc_info=None,
    )
    record.first = "first"  # type: ignore
    record.second = False  # type: ignore
    record.third = {"a": "b"}  # type: ignore
    record.fourth = 1.123  # type: ignore
    record.fifth = 1  # type: ignore
    record.sixth = ["a", "b"]  # type: ignore
    record.seventh = datetime.datetime(  # type: ignore
        2022, 1, 1, 11, 11, 11, tzinfo=datetime.timezone.utc
    )
    record.eigth = object  # type: ignore
    assert """"seventh": "2022-01-01T11:11:11+00:00""" in json_formatter.format(record)
