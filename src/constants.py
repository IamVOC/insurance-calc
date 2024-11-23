import enum


class Environment(enum.StrEnum):
    local = "local"
    staging = "staging"
    production = "production"
