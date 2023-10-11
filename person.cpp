#include <cstdlib>
// Person class 

class Person{
	public:
		Person(int);
		int get();
		void set(int);
		int fib(int n);		// public method that calls private method fib_help
	private:
		int fib_help(int n);	// computes fibonacci sequence recursively
		int age;
	};
 
Person::Person(int n){
	age = n;
	}
 
int Person::get(){
	return age;
	}
 
void Person::set(int n){
	age = n;
	}

// fib (public) and fib_help (private) are methods to recursively 
// calculate fib sequence
int Person::fib(int n) {
	return fib_help(n);
}

int Person::fib_help(int n) {
	if(n <= 1) return n;
	return fib_help(n-1) + fib_help(n-2);
}

extern "C"{
	Person* Person_new(int n) {return new Person(n);}
	int Person_get(Person* person) {return person->get();}
	void Person_set(Person* person, int n) {person->set(n);}
	void Person_delete(Person* person){
		if (person){
			delete person;
			person = nullptr;
			}
		}
	// C binding enables Python to call the fib method
	int Person_fib(Person* person, int n) {return person->fib(n);}
	}