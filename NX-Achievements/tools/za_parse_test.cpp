#include "../watcher/source/za_save.hpp"

#include <cstdio>
#include <fstream>
#include <iterator>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) {
        std::fprintf(stderr, "usage: %s <save-main>\n", argv[0]);
        return 2;
    }

    std::ifstream file(argv[1], std::ios::binary);
    if (!file) {
        std::fprintf(stderr, "cannot open %s\n", argv[1]);
        return 2;
    }
    std::vector<std::uint8_t> data((std::istreambuf_iterator<char>(file)), {});
    if (data.size() <= 0x20) {
        std::fprintf(stderr, "save too small\n");
        return 2;
    }

    // The trailing 32 bytes are the SHA-256 hash, not encrypted block data.
    data.resize(data.size() - 0x20);
    nxach::za::cryptStaticXorpad(data);

    nxach::za::BlockView dex;
    if (!nxach::za::parseBlocks(data, nxach::za::KPOKEDEX, dex)) {
        std::fprintf(stderr, "block parse failed\n");
        return 1;
    }
    if (!dex.found) {
        std::fprintf(stderr, "Pokedex block not found\n");
        return 1;
    }
    const int caught = nxach::za::countLumiosePokedex(dex);
    if (caught < 0) {
        std::fprintf(stderr, "invalid Pokedex block\n");
        return 1;
    }
    std::printf("blocks_ok=1 pokedex_size=%zu caught=%d/230\n", dex.size, caught);
    return 0;
}
