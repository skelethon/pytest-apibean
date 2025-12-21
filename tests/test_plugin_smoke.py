def test_plugin_loaded(pytestconfig):
    plugin = pytestconfig.pluginmanager.get_plugin("pytest_apibean")
    assert plugin is not None

def test_plugin_distinfo(pytestconfig):
    plugins = pytestconfig.pluginmanager.list_plugin_distinfo()
    plugin_modules = [dist for (dist, _) in plugins]
    import apibean.pytest
    assert apibean.pytest.plugin in plugin_modules
