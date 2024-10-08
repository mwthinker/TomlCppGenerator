#include "tetris_config.h"

int main() {
    config::Config config;
    config.loadFromTOML(toml::parse("config.toml"));

    return 0;
}
