from pytest import mark, fixture
from requests import Session, Response


class BaseSession(Session):
    def __init__(self, **kwargs):
        self.base_url = kwargs.pop('base_url')
        super().__init__(**kwargs)

    def request(self, method, url, **kwargs) -> Response:
        response = super().request(method, url=f'{self.base_url}{url}', **kwargs)
        return response


@fixture
def session():
    return BaseSession(base_url='http://localhost:8081')


def test_check_status_code(session):
    response = session.get('/')
    assert response.status_code == 200
