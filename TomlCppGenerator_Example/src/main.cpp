#include "tetris_config.h"

#include <fmt/printf.h>

using namespace toml::literals::toml_literals;

void useValue(toml::value value) {
    fmt::println("{}", value["width"]["value"].as_integer());
}

template <typename T>
requires cppgen::Table<T>
void testing() {

}

//  , productsList_{Vector<Config::Product>::create(data_["product"])}

int main() {
	toml::value root = toml::parse(R"(C:\Github\TomlCppGenerator\tetris.toml)");
	config::Config config{root};

	testing<config::Config::Product>();

	root["window"]["width"] = 1000;

	//config::Config config{toml::table{}};

	auto& w = config.getWindow();
	int width = config.getWindow().getWidth() + 999;
	try {
		config.getWindow().setWidth(width);
		toml::value vall = toml::table{};
		fmt::println("vall {}", toml::format(vall));
		fmt::println("config = {}", toml::format(config.getData()));
	} catch (const toml::serialization_error& e) {
		fmt::println("{}", e.what());
	}
	const auto& vvvvv = config.getProducts();
	for (const auto& product : config.getProducts()) {
		fmt::println("product: {}", product.getColor());
	}

	fmt::println("Cat {}", config.getBar().getFoo().getCat());

	auto p = config.getProducts().add();
	p.setColor("blue");

	auto aa = p;
	config.getProducts().add().setColor("red");

	static_assert(std::is_constructible_v<int, toml::type_config::floating_type>);

	auto& integers = config.getIntegersList();
	//integers.add();
	integers.size();
	integers.pop_back();

	//integers.push_back(1);

	//for (auto integer : integers) {
		//integer.set(100);
		//fmt::println("integer: {}", integer.get());
	//}
	//for (const auto& integer : integers) {
		//fmt::println("integer: {}", integer.get());
	//}

	auto v = toml::value{};
	config::Config::Product product{v};
	//config::Vector<config::Config::Product>::wrap(v);


	//valuee.getOr("width", 10);
    //config::Config config{toml::parse("config.toml")};
    //config.loadFromTOML(toml::parse("config.toml"));
	
	auto value = R"(
		[window]
		width = 10
		height = 20
	)";

    toml::value old = toml::parse_str(value);
	toml::value val = toml::find_or(old, "window", toml::table{});

	val["widthasddsa"] = 1;
	val["widthasddsa"] = "assad";

	val.contains("width");
	if (val.is_table()) {
		fmt::println("{}", val["width"].as_integer());
	} else {
		fmt::println("Not a table");
	}

	toml::value newValue;

	toml::type_config::integer_type intType;

	//int aaa = toml::get_or(val.at("width"), 5);
	auto bbbb = toml::find_or(val, "width", "asd");
	toml::value dddd;
	auto& cccc = dddd["value"];

	//auto bbbb = toml::find_or(val, "width", 5);

	/*
	newValue["window"]["width"] = 99;
    
    try {
        fmt::println("Old: {}", toml::format(old));
		fmt::println("New: {}", toml::format(newValue));
	} catch (const toml::type_error& e) {
		fmt::println("{}", e.what());
	}

    //fmt::println("lit = {}", lit.as_integer());
    */
    
    return 0;
}
