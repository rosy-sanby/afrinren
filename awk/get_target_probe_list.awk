NR==FNR {
list[i++]=$1;
next
}
{
for (j=i-1; j>=0;)
    print $1,list[j--]
}

