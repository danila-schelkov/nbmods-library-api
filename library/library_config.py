from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class LibraryConfig(BaseSettings):
    mods_path: Path = Path("mods")
    icons_path: Path = Path("icons")
    icons_url: HttpUrl = "https://donutquine.dev/nbmods/icons/"
    mod_extension: str = ".NullsBrawlAssets"

    model_config = SettingsConfigDict(toml_file="configs/library_config.toml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


config = LibraryConfig()
