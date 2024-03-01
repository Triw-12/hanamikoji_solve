#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
	int cpt = 0;
	int t1 = time(NULL);
	while (time(NULL) - t1 < 1)
	{
		// printf("%ld\n", time(NULL));
		cpt++;
	}
	printf("%ld\n", cpt);
	return 0;
}