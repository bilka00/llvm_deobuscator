int ext_call(int test);

int test_function()
{
    //srand(0);
    //int r = rand();
 
    int ret = ext_call(1);
    for(int i=0; i<10; i++)
        ret++;
    if (ret==10)
        return -1;
    return ret;
}
int ext_call(int test)
{
    return test*2;
}

int main()
{
	return test_function();
}