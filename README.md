# python_sonnenbatterie compatible (readonly) wrapper for package sonnen_api_v2
Install this wrapper package with sonnen_api_v2 package to use Home Assistant custom component "sonnenbatterie" by weltmeyer.

sonnen_api_v2 uses only the API read token from sonnen batterie admin portal.

Differs from weltmeter package in that it does not use the default user login setup used by  older batteries. User installer credentials for hass is not encouraged.

There are no API V1 calls, response is faked using API V2 results.

Notably, serial number and model number are not available from any API V2 endpoint.

pip install "git+https://github.com/MarkusBiggus/sonnen_api_v2.git"

pip install "git+https://github.com/MarkusBiggus/python_sonnenbatterie_api_v2.git" --target sonnenbatterie --no-deps
