#include "tetris_config.h"

#include <fmt/printf.h>

using namespace toml::literals::toml_literals;

void useValue(toml::value value) {
    fmt::println("{}", value["width"]["value"].as_integer());
}

int main() {
    config::Config config;
    //config.loadFromTOML(toml::parse("config.toml"));

	auto value = R"(
		[window]
		width = 10
		height = 20
	)";

    const toml::value old = toml::parse_str(value);
    auto newValue = old;
	newValue["window"]["width"] = 99;
    
    try {
        fmt::println("Old: {}", toml::format(old));
		fmt::println("New: {}", toml::format(newValue));
	} catch (const toml::type_error& e) {
		fmt::println("{}", e.what());
	}

    //fmt::println("lit = {}", lit.as_integer());
    
    return 0;
}
