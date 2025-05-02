import os
import re
from urllib.parse import urljoin
from uuid import UUID
from zipfile import ZipFile

from pydantic import BaseModel, Field, HttpUrl

from library.cache_decorator import time_cache
from library.library_config import config

type LocalizationObject = dict[str, str]
type LocalizedField = LocalizationObject | str

UUID_PATTERN = re.compile(
    "Modification-Id: ([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
)


class ModMetaInfo(BaseModel, extra="ignore"):
    class Config:
        @staticmethod
        def _add_meta_prefix(field_name: str) -> str:
            return f"@{field_name}"

        alias_generator = _add_meta_prefix
        validate_by_name = True

    title: LocalizedField
    description: LocalizedField
    author: LocalizedField = "<b><i>unknown author</i><b/>"
    gv: int


class LibraryMod(BaseModel):
    id: UUID
    meta: ModMetaInfo
    icon_url: HttpUrl | None = None
    size: int


class Index(BaseModel):
    library: list[LibraryMod] = Field(default_factory=list)
    categories: dict[str, LocalizedField] | None = None


@time_cache(1800)
def get_index() -> Index:
    index = Index()

    config.icons_path.mkdir(parents=True, exist_ok=True)

    for file in os.listdir(config.mods_path):
        if not file.endswith(".NullsBrawlAssets"):
            continue

        mod_path = config.mods_path / file

        with ZipFile(mod_path) as zip_file:
            manifest = zip_file.read("META-INF/MANIFEST.MF").decode()
            content_json = zip_file.read("content.json")

            mod_id = UUID_PATTERN.search(manifest).group(1)

            library_mod = LibraryMod(
                id=mod_id,
                meta=ModMetaInfo.model_validate_json(content_json),
                size=os.path.getsize(mod_path),
            )

            if "icon.png" in zip_file.namelist():
                icon = zip_file.read("icon.png")
                icon_filename = mod_id + ".png"

                with open(config.icons_path / icon_filename, "wb") as icon_file:
                    icon_file.write(icon)

                library_mod.icon_url = HttpUrl(
                    urljoin(str(config.icons_url), icon_filename)
                )

            index.library.append(library_mod)

    return index
