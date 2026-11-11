"""Tests for the positive message generator (/positive and /pm).

Run with: python -m pytest tests/test_positive_message.py
"""

from flask import template_rendered
from markupsafe import escape


def test_positive_page_loads(client):
    response = client.get("/positive")
    assert response.status_code == 200


def test_pm_post_returns_success(client):
    response = client.post("/pm")
    assert response.status_code == 200


def test_pm_passes_a_message_to_the_template(app, client):
    rendered = []

    def record(sender, template, context, **extra):
        rendered.append((template, context))

    with template_rendered.connected_to(record, app):
        response = client.post("/pm")

    assert response.status_code == 200
    pm_renders = [ctx for tpl, ctx in rendered if tpl.name == "positivemessage.html"]
    assert pm_renders, "positivemessage.html was not rendered"
    message = pm_renders[-1].get("message")
    assert isinstance(message, str) and message
    # The template prints the message it was given (HTML-escaped by Jinja).
    assert str(escape(message)).encode() in response.data
