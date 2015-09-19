{
if (!id[$2]) #if this asn hasn't been seen yet
{
    id[$2]=$1;
    country[$2]=$3;
    count[$2]++;
    print id[$2],$2,country[$2];
} else if (count[$2]<2) { #we only want two probes per asn
    id[$2]=$1;
    country[$2]=$3;
    count[$2]++;
    print id[$2],$2,country[$2]
    
}
}
#END{
#for (var in id)
#    print id[var],as[var],var
#}
