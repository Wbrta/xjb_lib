#ifndef SKIP_LIST_H
#define SKIP_LIST_H

#include <initializer_list>

template<typename T>
typedef struct skip_list_structure {
public:
	skip_list_structure(T _value) : value(_value) {
		level = 0;
		forward = nullptr;
	}
private:
	using SKIP_LIST_POINTER = skip_list_structure<T>*;

	T value;
	int level;
	SKIP_LIST_POINTER forward;
};

template<typename T>
class skip_list {
public:
	skip_list();
	skip_list(initializer_list<T>&);
	virtual ~skip_list();
private:
	using skip_list_pointer = skip_list_structure<T>*;
	skip_list_pointer skip_list_header;
};

#endif