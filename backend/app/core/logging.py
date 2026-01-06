import logging


def configure_logging(app_env: str) -> None:
    env = (app_env or "dev").lower()
    is_prod = env in {"prod", "production"}
    level = logging.INFO if is_prod else logging.DEBUG
    log_format = (
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
        if is_prod
        else "%(levelname)s %(name)s: %(message)s"
    )
    logging.basicConfig(level=level, format=log_format)
