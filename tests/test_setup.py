# 3rd party
from sphinx.events import EventListener
from sphinx_toolbox.testing import run_setup

# this package
import sphinx_autofixture


def test_setup():
	setup_ret, directives, roles, additional_nodes, app = run_setup(sphinx_autofixture.setup)
	assert setup_ret == {
			"version": sphinx_autofixture.__version__,
			"parallel_read_safe": True,
			}

	assert app.registry.documenters["fixture"] == sphinx_autofixture.FixtureDocumenter

	assert app.events.listeners == {
			"config-inited": [EventListener(id=0, handler=sphinx_autofixture.validate_config, priority=500)],
			}

	assert "fixture" in app.registry.domains["py"].object_types
