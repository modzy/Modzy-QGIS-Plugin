from modzy import ApiClient
from qgis.core import QgsApplication, QgsAuthMethodConfig

def get_client():
	auth_configs = QgsApplication.authManager().availableAuthMethodConfigs()
	auth_mgr = QgsApplication.authManager()
	auth_cfg = QgsAuthMethodConfig()
	client = None 

	for each in auth_configs:
		if (auth_configs[each].name() == 'ModzyAPI'):
			auth_id = auth_configs[each].id()
			api_url = auth_configs[each].uri()
			auth_mgr.loadAuthenticationConfig(auth_id, auth_cfg, True)
			api_key = auth_cfg.configMap()['password']

			client = ApiClient(base_url=api_url, api_key=api_key)
			
	return client

