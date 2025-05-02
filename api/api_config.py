from pydantic.networks import IPvAnyAddress
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class ApiConfig(BaseSettings):
    reload: bool = False
    host: IPvAnyAddress = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(toml_file="configs/api_config.toml")

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


config = ApiConfig()
