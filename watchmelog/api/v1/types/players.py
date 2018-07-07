from apistar import types, validators


class RegisterPlayer(types.Type):
    battletag: str = validators.String(description="Your Battle.net Tag")
    password: str = validators.String(
        min_length=12, description="Password used to authenticate with the API."
    )
    platform: str = validators.String(
        enum=["PC", "XBOX", "PS4"], description="Platform you're playing on."
    )
    region: str = validators.String(
        enum=["US", "EU", "ASIA"], description="Region you're playing on."
    )


class Login(types.Type):
    password: str = validators.String(description="Your registered password.")
