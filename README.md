# RedForester API client

Asynchronous client for RedForester API.

[PyPI package](https://pypi.org/project/rf-api-client/)

## Development

Install all requirements
```bash
pip install -e .[dev]
```

Lint
```
flake8 --max-line-length=120 examples rf_api_client tests
```

Run tests

Setup environment variables:
- rf_api_client_username
- rf_api_client_password
- rf_api_client_base_url (optional)

And run with
```
pytest
```
