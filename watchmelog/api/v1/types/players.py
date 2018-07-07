from apistar import types, validators

from watchmelog.api.v1.models.players import PLATFORM_CHOICES, REGION_CHOICES


class RegisterPlayer(types.Type):
    battletag: str = validators.String(description="Your Battle.net Tag")
    password: str = validators.String(
        min_length=12, description="Password used to authenticate with the API."
    )
    default_platform: str = validators.String(
        enum=PLATFORM_CHOICES, description="Platform you're playing on."
    )
    default_region: str = validators.String(
        enum=REGION_CHOICES, description="Region you're playing on."
    )


class Login(types.Type):
    password: str = validators.String(description="Your registered password.")
