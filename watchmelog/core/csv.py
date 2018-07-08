import csv
import io
import pprint
from typing import List, Tuple, Any, Union

from watchmelog.models.games import HERO_CHOICES, Game, MAP_CHOICES
from watchmelog.models.players import Player


_VALID_DAY = ["weekday", "weekend"]
_VALID_TIME = ["morning", "afternoon", "evening", "night"]
_VALID_RESULT = ["win", "loss", "draw"]


def _eval_bool(value: str) -> bool:
    if value.lower() in ["y", "yes", "true", "t", "ok", "1"]:
        return True
    return False


def import_raw_csv(
    player: Player, season: int, raw_matches: str
) -> Tuple[bool, List[str]]:
    """
    Imports a csv file of matches for a specific season.

    :param player:
    :param season:
    :param raw_matches: Raw content of the CSV file.

    :return:
    """
    fieldnames = raw_matches[: raw_matches.index("\n")].lower().split(",")
    raw_matches = raw_matches[raw_matches.index("\n") + 1 :]

    raw_matches = csv.DictReader(io.StringIO(raw_matches), fieldnames=fieldnames)

    matches = []
    errors = []

    for index, row in enumerate(raw_matches):
        line_prefix = f"Line {index + 1}:"
        line_errors = []

        # Validation
        is_placement_match = _eval_bool(row.get("placement", ""))

        if not row.get("rank") and not is_placement_match:
            line_errors.append(f"{line_prefix} Missing rank for non-placement match")

        # if row.get("rank") and is_placement_match:
        #     line_errors.append(f"{line_prefix} Cannot set rank on placement match")

        if "rank" in row and not is_placement_match:
            try:
                rank = int(row["rank"])
                if not 0 <= rank <= 5000:
                    raise ValueError
            except ValueError:
                line_errors.append(
                    f'{line_prefix} Invalid value "{row["rank"]}" for column "rank"'
                )

        if is_placement_match and "result" not in row:
            line_errors.append(f"{line_prefix} Missing result for placement match")

        if "day" in row and row["day"] not in _VALID_DAY:
            line_errors.append(
                f'{line_prefix} Invalid value "{row["day"]}" for column "day"'
            )

        if "time" in row and row["time"] not in _VALID_TIME:
            line_errors.append(
                f'{line_prefix} Invalid value "{row["time"]}" for column "time"'
            )

        if "result" in row and row["result"] not in _VALID_RESULT:
            line_errors.append(
                f'{line_prefix} Invalid value "{row["result"]}" for column "result"'
            )

        if line_errors:
            errors.extend(line_errors)
            continue

        # Cleanup
        if "ally thrower" in row:
            row["ally thrower"] = _eval_bool(row["ally thrower"])
        if "enemy thrower" in row:
            row["enemy thrower"] = _eval_bool(row["enemy thrower"])
        if "ally leaver" in row:
            row["ally leaver"] = _eval_bool(row["ally leaver"])
        if "enemy leaver" in row:
            row["enemy leaver"] = _eval_bool(row["enemy leaver"])
        if "placement" in row:
            row["placement"] = _eval_bool(row["placement"])

        matched_heroes = []
        unmatched_heroes = []
        if "heroes" in row:
            heroes = [h.strip() for h in row["heroes"].split(",")]
            for hero in heroes:
                if hero not in HERO_CHOICES:
                    unmatched_heroes.append(hero)
                else:
                    matched_heroes.append(hero)

        comment = row.get("comment", "")
        if unmatched_heroes:
            comment += f'\nCould not match heroes: {",".join(unmatched_heroes)}'

        if "map" in row:
            matched_map = row["map"] in MAP_CHOICES
            if not matched_map:
                comment += f'\nCould not match map: {row["map"]}'
                row["map"] = None

        group = []
        if "group" in row:
            group = [r.strip() for r in row["group"].split(",")]

        match_data = {
            "sr": int(row.get("rank")) if row.get("rank") else None,
            "result": row.get("result"),
            "placement": row.get("placement"),
            "map": row.get("map"),
            "heroes": matched_heroes,
            "comment": comment,
            "thrower_team": row.get("ally thrower"),
            "thrower_enemy_team": row.get("enemy thrower"),
            "leaver_team": row.get("ally leaver"),
            "leaver_enemy_team": row.get("enemy leaver"),
            "group_with": group,
            "player": player,
            "season": season,
            "platform": player.default_platform,
            "region": player.default_region,
        }
        matches.append(match_data)

    if errors:
        return False, errors

    # Use session region here if defined?
    Game.objects(
        player=player,
        season=season,
        region=player.default_region,
        platform=player.default_platform,
    ).delete()

    for match in matches:
        Game(**match).save()

    return True, []
