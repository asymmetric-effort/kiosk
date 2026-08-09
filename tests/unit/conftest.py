import pathlib

import pytest
import yaml
from jinja2 import Environment, FileSystemLoader, Undefined


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]


class _PermissiveUndefined(Undefined):
    """Return empty string for undefined variables instead of raising."""

    def __str__(self):
        return ""

    def __iter__(self):
        return iter([])

    def __bool__(self):
        return False


def _load_defaults(role_name):
    defaults_path = PROJECT_ROOT / "roles" / role_name / "defaults" / "main.yml"
    if defaults_path.exists():
        with open(defaults_path) as f:
            return yaml.safe_load(f) or {}
    return {}


def _render_template(role_name, template_name, extra_vars=None):
    template_dir = PROJECT_ROOT / "roles" / role_name / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=_PermissiveUndefined,
    )

    template = env.get_template(template_name)

    context = _load_defaults(role_name)
    context.setdefault("ansible_managed", "Ansible managed")
    context.setdefault("ansible_distribution_release", "jammy")
    if extra_vars:
        context.update(extra_vars)

    return template.render(**context)


@pytest.fixture
def render():
    return _render_template
