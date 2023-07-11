from collections import OrderedDict
import os
from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import MINOR, PATCH, MAJOR
from commitizen.cz.utils import multiple_line_breaker, required_validator


def parse_scope(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="El scope es requerido.")

def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="El asunto de cambio es requerido.")


class EmoticonCz(BaseCommitizen):

    bump_pattern = r"^(((🚨 BREAKING CHANGE|✨ feat|🪲 fix|♻️ refactor|⚡ perf)(\[.+\])(!)?))"
    bump_map = OrderedDict(
        (
            (r"^.+!$", MAJOR),
            (r"^✨ feat", MINOR),
            (r"^🪲 fix", PATCH),
            (r"^♻️ refactor", PATCH),
            (r"^⚡ perf", PATCH),
        )
    )
    bump_map_major_version_zero = OrderedDict(
        (
            (r"^.+!$", MINOR),
            (r"^✨ feat", MINOR),
            (r"^🪲 fix", PATCH),
            (r"^♻️ refactor", PATCH),
            (r"^⚡ perf", PATCH),
        )
    )
    commit_parser = r"(?P<change_type>✨ feat|🪲 fix|📝 docs|🎨 style|♻️ refactor|⚡ perf|🧪 test|📦 build|🚀 ci|🔧 chore|⏪ revert)(?:\[(?P<scope>[^()\s]*)\])(?P<breaking>!)?(?P<message>[^()\s]*)(?:\((?P<footer>.*)\))?"
    change_type_map = {
        "✨ feat": "✨ Feat",
        "🪲 fix": "🪲 Fix",
        "♻️ refactor": "♻️ Refactor",
        "⚡ perf": "⚡ Perf",
    }
    changelog_pattern = r"^(🚨 BREAKING CHANGE|✨ feat|🪲 fix|📝 docs|🎨 style|♻️ refactor|⚡ perf|🧪 test|📦 build|🚀 ci|🔧 chore|⏪ revert)(.*)?(!)?"
    change_type_map = {"✨ feat": "✨ Feat", "🪲 fix": "🪲 Fix", "♻️ refactor": "♻️ Refactor", "⚡ perf": "⚡ Perf"}

    def questions(self) -> list:
        return [
            {
                "type": "list",
                "name": "prefix",
                "message": "Seleccione el tipo de cambio que va a realizar",
                "choices": [
                    {
                        "value": "🪲 fix",
                        "name": "🪲 fix: Cuando se arregla un error. Relacionado con PATCH en SemVer.",
                        "key": "x",
                    },
                    {
                        "value": "✨ feat",
                        "name": "✨ feat: Cuando se añade una nueva funcionalidad. Relacionado con MINOR en SemVer.",
                        "key": "f",
                    },
                    {
                        "value": "📝 docs",
                        "name": "📝 docs: Cuando solo se modifica documentacion.",
                        "key": "d",
                    },
                    {
                        "value": "🎨 style",
                        "name": (
                            "🎨 style: Cambios de legibilidad o formateo de codigo que no afecta a funcionalidad. (white-space, formatting, missing semi-colons, etc)."
                        ),
                        "key": "s",
                    },
                    {
                        "value": "♻️ refactor",
                        "name": (
                            "♻️ refactor: Cambio de codigo que no corrige errores ni añade funcionalidad, pero mejora el codigo."
                        ),
                        "key": "r",
                    },
                    {
                        "value": "⚡ perf",
                        "name": "⚡ perf: Usado para mejoras de rendimiento.",
                        "key": "p",
                    },
                    {
                        "value": "🧪 test",
                        "name": (
                            "🧪 test: Si añadimos o arreglamos tests existentes."
                        ),
                        "key": "t",
                    },
                    {
                        "value": "📦 build",
                        "name": (
                            "📦 build: Cuando el cambio afecta al compilado del proyecto o dependencias externas (ejemplo: pip, docker, npm)."
                        ),
                        "key": "b",
                    },
                    {
                        "value": "🚀 ci",
                        "name": (
                            "🚀 ci: el cambio afecta a ficheros de configuracion y scripts relacionados con la integracion continua (ejemplo: .gitlabc-ci.yaml)."
                        ),
                        "key": "c",
                    },
                    {
                        "value": "🔧 chore",
                        "name": (
                            "🔧 chore: tareas rutinarias que no sean especificas de una feature o un error (ejemplo: add .gitignore, instalar una dependencia, primer commit)."
                        ),
                        "key": "h",
                    },
                    {
                        "value": "⏪ revert",
                        "name": (
                            "⏪ revert: si el commit revierte un commit anterior. Deberia indicarse el hash del commit que se revierte."
                        ),
                        "key": "z",
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "🚩 Cual es el alcance de este cambio? (nombre de clase o archivo): (es obligatorio colocar un scope)\n"
                ),
                "filter": parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "✏️ Escriba un resumen breve e imperativo de los cambios en el codigo: (minusculas y sin punto)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "📄 Proporcione informacion contextual adicional sobre los cambios de codigo: (pulse [intro] para omitir)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "🚨 Se trata de un CAMBIO IMPORTANTE? Relacionado con MAJOR en SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "💬 Pie de pagina. Informacion sobre cambios de ultima hora y problemas de referencia que cierra esta confirmación: (pulse [enter] para saltar)\n"
                ),
            },
        ]

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]
        breaking = ""

        if scope:
            scope = f"[{scope}]"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE: {footer}"
            breaking = "!"
        if footer:
            footer = f"\n\n({footer})"

        message = f"{prefix}{scope}{breaking}: {subject}{body}{footer}"

        return message

    def example(self) -> str:
        return (
            "fix[main.py]: correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "(closes issue #12)"
        )

    def schema(self) -> str:
        return (
            "<type>[<scope>]: <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: <footer>)"
        )

    def schema_pattern(self) -> str:
        return r"(✨ feat|🪲 fix|📝 docs|🎨 style|♻️ refactor|⚡ perf|🧪 test|📦 build|🚀 ci|🔧 chore|⏪ revert|🔖 release)(\[[^()\s]{3,}\])(!)?:\s([^()\s]*)(\((.*)\))?"

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content