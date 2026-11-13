"""Tests for the password generator entropy parameter validation.

The /generator endpoint accepts an optional ``entropy`` form field.
Valid values are integers in the range [0, 5]; missing values default
to 0; non-numeric and out-of-range values must be rejected with HTTP
400 instead of raising unhandled exceptions.

Run from the repository root:

    pip install -r requirements.txt pytest
    python -m pytest tests/test_password_generator.py
"""

import os
import sys

import pytest

# Make the repository root importable so `import app` works from tests/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app  # noqa: E402


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


class TestGeneratorEntropyValidation:
    """Tests for entropy parameter handling on POST /generator."""

    def test_valid_entropy_zero(self, client):
        """Entropy value 0 is accepted."""
        response = client.post('/generator', data={'entropy': '0'})
        assert response.status_code == 200
        assert b'Your password' in response.data or b'<em>' in response.data

    def test_valid_entropy_one(self, client):
        """Entropy value 1 is accepted."""
        response = client.post('/generator', data={'entropy': '1'})
        assert response.status_code == 200

    def test_valid_entropy_two(self, client):
        """Entropy value 2 is accepted."""
        response = client.post('/generator', data={'entropy': '2'})
        assert response.status_code == 200

    def test_valid_entropy_three(self, client):
        """Entropy value 3 is accepted."""
        response = client.post('/generator', data={'entropy': '3'})
        assert response.status_code == 200

    def test_valid_entropy_four(self, client):
        """Entropy value 4 is accepted."""
        response = client.post('/generator', data={'entropy': '4'})
        assert response.status_code == 200

    def test_valid_entropy_five(self, client):
        """Entropy value 5 is accepted."""
        response = client.post('/generator', data={'entropy': '5'})
        assert response.status_code == 200

    def test_missing_entropy_defaults_to_zero(self, client):
        """When entropy is not provided, it defaults to 0 without error."""
        response = client.post('/generator', data={})
        assert response.status_code == 200

    def test_empty_entropy_defaults_to_zero(self, client):
        """An empty string entropy defaults to 0 without error."""
        response = client.post('/generator', data={'entropy': ''})
        assert response.status_code == 200

    def test_nonnumeric_string_rejected(self, client):
        """Non-numeric strings are rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': 'abc'})
        assert response.status_code == 400

    def test_float_string_rejected(self, client):
        """Float-like strings are rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': '2.5'})
        assert response.status_code == 400

    def test_negative_out_of_range_rejected(self, client):
        """Negative entropy values are rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': '-1'})
        assert response.status_code == 400

    def test_positive_out_of_range_rejected(self, client):
        """Entropy values greater than 5 are rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': '6'})
        assert response.status_code == 400

    def test_large_positive_out_of_range_rejected(self, client):
        """Large positive entropy values are rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': '999'})
        assert response.status_code == 400

    def test_whitespace_string_rejected(self, client):
        """Whitespace-only strings are rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': '   '})
        assert response.status_code == 400

    def test_null_string_rejected(self, client):
        """String literal 'null' is rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': 'null'})
        assert response.status_code == 400

    def test_none_entropy_handled_gracefully(self, client):
        """None entropy is handled gracefully and defaults to 0."""
        response = client.post('/generator', data={'entropy': None})
        assert response.status_code == 200

    def test_plus_prefix_rejected(self, client):
        """Malformed number with ++ prefix is rejected with HTTP 400."""
        response = client.post('/generator', data={'entropy': '++5'})
        assert response.status_code == 400

    def test_leading_zeros_accepted(self, client):
        """Entropy with leading zeros parses as integer and is accepted."""
        response = client.post('/generator', data={'entropy': '00'})
        assert response.status_code == 200

    def test_signed_positive_entropy_accepted(self, client):
        """Positive signed integer strings (e.g. '+3') parse as integers and return 200."""
        for val in ['+0', '+3', '+5']:
            response = client.post('/generator', data={'entropy': val})
            assert response.status_code == 200

    def test_negative_zero_entropy_accepted(self, client):
        """Entropy '-0' parses to 0 and returns 200."""
        response = client.post('/generator', data={'entropy': '-0'})
        assert response.status_code == 200

    def test_entropy_with_surrounding_whitespace_accepted(self, client):
        """Entropy integer with leading/trailing whitespace parses as int and returns 200."""
        response = client.post('/generator', data={'entropy': ' 3 '})
        assert response.status_code == 200

    def test_error_description_returned_on_400(self, client):
        """Aborted 400 response includes the descriptive error message."""
        response = client.post('/generator', data={'entropy': 'invalid'})
        assert response.status_code == 400
        assert b'Invalid entropy value' in response.data

    def test_special_characters_rejected(self, client):
        """Strings consisting of special characters are rejected with HTTP 400."""
        for val in ['!@#', '$', '%', '&', '*(#)']:
            response = client.post('/generator', data={'entropy': val})
            assert response.status_code == 400

    def test_hex_and_scientific_notation_rejected(self, client):
        """Hexadecimal or scientific notation string representations are rejected with HTTP 400."""
        for val in ['0x1', '0x5', '1e2', '1e0']:
            response = client.post('/generator', data={'entropy': val})
            assert response.status_code == 400

    def test_boolean_and_special_string_literals_rejected(self, client):
        """Boolean or literal values as strings are rejected with HTTP 400."""
        for val in ['True', 'false', 'None', 'undefined', 'inf', '-inf', 'nan']:
            response = client.post('/generator', data={'entropy': val})
            assert response.status_code == 400

    def test_float_variations_rejected(self, client):
        """Floating point number string formats are rejected with HTTP 400."""
        for val in ['0.0', '3.0', '5.0', '-0.1', '5.1']:
            response = client.post('/generator', data={'entropy': val})
            assert response.status_code == 400

    def test_extreme_boundary_integers_rejected(self, client):
        """Extreme large or small integers are rejected with HTTP 400."""
        for val in ['-999999999', '1000000000', '-2147483648', '2147483647']:
            response = client.post('/generator', data={'entropy': val})
            assert response.status_code == 400

    def test_extra_form_fields_ignored(self, client):
        """Unrelated form fields alongside entropy do not cause issues."""
        response = client.post('/generator', data={'entropy': '3', 'csrf_token': 'secret123', 'other': 'value'})
        assert response.status_code == 200

    def test_multiple_entropy_fields_handled(self, client):
        """Form submission with multiple values for entropy uses first valid value."""
        response = client.post('/generator', data={'entropy': ['2', '4']})
        assert response.status_code == 200

    def test_multipart_form_data_submission(self, client):
        """Submissions with multipart/form-data content type succeed."""
        response = client.post('/generator', data={'entropy': '2'}, content_type='multipart/form-data')
        assert response.status_code == 200


class TestGeneratorContentAndBehavior:
    """Tests for rendered content, password generation, and HTTP methods."""

    def test_get_request_renders_form(self, client):
        """GET /generator returns 200 and renders the password generator page."""
        response = client.get('/generator')
        assert response.status_code == 200
        assert b'<title>Password Generator</title>' in response.data
        assert b'name="entropy"' in response.data

    def test_all_entropy_levels_generate_non_empty_passwords(self, client):
        """Entropy levels 0 through 5 each render a non-empty generated password."""
        for level in range(6):
            response = client.post('/generator', data={'entropy': str(level)})
            assert response.status_code == 200
            assert b'Your password' in response.data
            assert b'id="generated-password"' in response.data

    def test_consecutive_generations_vary(self, client):
        """Multiple generation requests produce varied passwords due to randomization."""
        passwords = set()
        for _ in range(5):
            response = client.post('/generator', data={'entropy': '0'})
            assert response.status_code == 200
            # Extract text inside <em>...</em>
            html = response.get_data(as_text=True)
            if '<em>' in html and '</em>' in html:
                pwd = html.split('<em>')[1].split('</em>')[0]
                passwords.add(pwd)
        # With random words and digits, at least 2 distinct passwords should be generated across 5 tries
        assert len(passwords) >= 2

    @pytest.mark.parametrize('method', ['put', 'delete', 'patch'])
    def test_disallowed_http_methods(self, client, method):
        """HTTP methods other than GET and POST return HTTP 405 Method Not Allowed."""
        http_func = getattr(client, method)
        response = http_func('/generator')
        assert response.status_code == 405
