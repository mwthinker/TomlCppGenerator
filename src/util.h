#ifndef UTIL_H
#define UTIL_H

#include <toml.hpp>

#include <vector>
#include <concepts>

namespace config {

    template <typename T>
    concept InputIterator = std::input_iterator<T>;

    template <typename Func, typename Iterator>
    concept TransformFunc = std::input_iterator<Iterator> && requires(Func f, Iterator it) {
        { f(*it) } -> std::convertible_to<std::invoke_result_t<Func, typename std::iterator_traits<Iterator>::reference>>;
    };

    template <InputIterator Iterator, TransformFunc<Iterator> Func>
    class TransformIterator {
    public:
        using iterator_category = std::iterator_traits<Iterator>::iterator_category;
        using value_type = std::invoke_result_t<Func, typename std::iterator_traits<Iterator>::reference>;
        using difference_type = std::iterator_traits<Iterator>::difference_type;
        using pointer = value_type*;
        using reference = value_type;

    public:
        TransformIterator(Iterator iter, Func f)
            : current{iter}
            , func{f} {
        }

        reference operator*() const {
            return func(*current);
        }

        TransformIterator& operator++() {
            ++current;
            return *this;
        }

        TransformIterator operator++(int) {
            TransformIterator temp = *this;
            ++(*this);
            return temp;
        }

        bool operator==(const TransformIterator& other) const {
            return current == other.current;
        }

        bool operator!=(const TransformIterator& other) const {
            return !(*this == other);
        }

    private:
        Iterator current;
        Func func;
    };

    template<typename T>
    concept Table = std::is_constructible_v<T, toml::value&>;

    template <typename Type>
    class Vector {
    public:
        static Vector create(toml::value& value) {
            if (!value.is_array()) {
                // TODO! Maybe throw an exception here or warn?
                value = toml::array{};
            }

            return Vector{value.as_array()};
        }

        explicit Vector(toml::array& value)
            : data_{std::ref(value)} {
        }

        Vector(Vector&) = delete;
        Vector& operator=(Vector&) = delete;

		/// @brief Add a new element to the vector (only available if the element is a Table toml type)
		/// @return the new element
        Type add() requires Table<Type> {
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

        auto pop_back() {
            data_.get().pop_back();
        }

        auto size() const {
            return data_.get().size();
        }

    private:
        static Type wrap(toml::value& value) {
            if constexpr (std::is_same_v<Type, toml::type_config::integer_type>) {
                return value.as_integer();
            } else if constexpr (std::is_same_v<Type, toml::type_config::string_type>) {
                return value.as_string();
            } else if constexpr (std::is_same_v<Type, toml::type_config::boolean_type>) {
                return value.as_boolean();
            } else if constexpr (std::is_same_v<Type, toml::type_config::floating_type>) {
                return value.as_floating();
            } else {
                static_assert(std::is_constructible_v<Type, toml::value&>, "Type must be constructible from toml::value&");
                return Type{value};
            }
        }

        std::reference_wrapper<toml::array> data_;
    };

}

#endif
