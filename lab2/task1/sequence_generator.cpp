#include <bitset>
#include <fstream>
#include <random>


void generate_sequence()
{
	std::random_device rd;
	std::mt19937_64 gen;

	uint64_t first_64 = gen();
	uint64_t last_64 = gen();

	std::bitset<64> first_bin(first_64);
	std::bitset<64> last_bin(last_64);

	std::ofstream file("cpp_sequence.txt");
	file << first_bin << last_bin;
	file.close();
}


int main()
{
	generate_sequence();

	return 0;
}