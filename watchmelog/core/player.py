import requests

from watchmelog.models.players import Player, ApiKey


def get_player_from_api_key(api_key: str) -> Player:
    api_key: ApiKey = ApiKey.objects(key=api_key).first()
    player = None
    if api_key:
        player = api_key.player
    return player


def create_or_update_player(access_token: str, region: str) -> Player:
    player_profile_req = requests.get(
        f"https://{region}.api.battle.net/account/user",
        params={"access_token": access_token},
    )
    player_profile_req.raise_for_status()
    player_profile = player_profile_req.json()

    player: Player = Player.objects(blizzard_id=player_profile["id"]).first()

    if player:
        player.update(battletag=player_profile["battletag"])
    else:
        player = Player(
            battletag=player_profile["battletag"],
            blizzard_id=player_profile["id"],
            default_region=region,
        ).save()

    return player


def ensure_api_key_for_player(player: Player) -> ApiKey:
    api_key = ApiKey.objects(player=player).first()
    if not api_key:
        api_key = ApiKey(player=player).save()
    return api_key
