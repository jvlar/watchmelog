from watchmelog.config import app_config


def get_curr_season() -> int:
    return int(app_config.current_season)


def form_status_class(form) -> str:
    if form.errors:
        return "error"
