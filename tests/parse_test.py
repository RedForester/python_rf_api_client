from rf_api_client.models.base_model import ApiBaseModel


def test_default_if_null():
    class TestClass(ApiBaseModel):
        field: int = 10

    obj = TestClass(**{})
    assert obj.field == 10

    obj = TestClass(**{"field": None})
    assert obj.field == 10

    obj = TestClass(**{"field": 42})
    assert obj.field == 42
