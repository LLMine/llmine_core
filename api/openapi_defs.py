from drf_spectacular.extensions import OpenApiAuthenticationExtension


class KnoxTokenScheme(OpenApiAuthenticationExtension):
    target_class = "knox.auth.TokenAuthentication"
    name = "knoxTokenAuth"
    match_subclasses = True
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": ('Token-based authentication with required prefix "Token"'),
        }
