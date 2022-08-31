#include <stdio.h>
#include "../../build/sample_plugin.h"

int main(int argc, char *argv[]) {
    int limit = 6;
    hello_world();

    printf("called from c: summing 0 to %i = %i\n",limit, sumup(limit));
    return 0;
}