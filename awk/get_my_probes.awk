{
if (!id[$2]) #if this asn hasn't been seen yet
{
    id[$2]=$1;
    lat[$2] = $4;
    long[$2]=$5;
    count[$2]++;
    print id[$2],$2,lat[$2],long[$2];
} else if (count[$2]<2) { #we only want two probes per asn
    id[$2]=$1;
    lat[$2] = $4;
    long[$2]
    count[$2]++;
    print id[$2],$2,lat[$2],long[$2]
    
}
}
#END{
#for (var in id)
#    print id[var],as[var],var
#}
