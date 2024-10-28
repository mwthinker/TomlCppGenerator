#ifndef UTIL_H
#define UTIL_H

#include <toml.hpp>

#include <vector>

namespace config {

    template <typename Iterator, typename Func>
    class TransformIterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = decltype(std::declval<Func>()(*std::declval<Iterator>()));
        using difference_type = std::ptrdiff_t;
        using pointer = value_type*;
        using reference = value_type&;

    private:
        Iterator current;
        Func func;

    public:
        // Constructor
        TransformIterator(Iterator iter, Func f) : current(iter), func(f) {}

        // Dereference operator applies the transformation function
        value_type operator*() const {
            return func(*current);
        }

        // Pre-increment
        TransformIterator& operator++() {
            ++current;
            return *this;
        }

        // Post-increment
        TransformIterator operator++(int) {
            TransformIterator temp = *this;
            ++(*this);
            return temp;
        }

        // Equality comparison
        bool operator==(const TransformIterator& other) const {
            return current == other.current;
        }

        // Inequality comparison
        bool operator!=(const TransformIterator& other) const {
            return !(*this == other);
        }
    };

	template <typename Type>
	class Vector {
	public:
		Vector() = default;

		static Vector create(toml::value& value) {
            if (!value.is_array()) {
				// TODO! Maybe throw an exception here or warn?
                value = toml::array{};
			}

            int size = value.as_array().size();

			return Vector{value.as_array()};
		}

		Vector(toml::array& value)
			: data_{std::ref(value)} {
		}

        static Type wrap(toml::value& value) {
            return Type{value};  // Assuming W can be constructed from T
        }

        Type add() {
			auto& t = data_.get().emplace_back();
            return Type{t};
		}

        auto begin() {
            return TransformIterator{data_.get().begin(), wrap};
        }

        auto begin() const {
            return data_.get().begin();
        }

        auto end() {
			return TransformIterator{data_.get().end(), wrap};
        }

        auto end() const {
            return data_.get().end();
        }

        auto cbegin() const {
            return data_.get().cbegin();
        }

        auto cend() const {
            return data_.get().cend();
        }
    private:
        std::reference_wrapper<toml::array> data_;
	};

}

#endif
