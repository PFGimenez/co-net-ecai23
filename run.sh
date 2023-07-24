#!/bin/sh

cd datasets
rm *.csv.*

# compress
for d in $(ls *.csv); do
    echo "Compressing $d..."
    gzip -9 -k $d > /dev/null # deflate
    bzip2 -9 -k $d > /dev/null # bzip2
    lzma -9 -k $d > /dev/null # LZMA
    p7zip -k $d > /dev/null # LZMA2
    zstd -19 -k $d 2> /dev/null # zstd
done

echo -n "    Compression rate:"
# compute compression rate
for d in $(ls *.csv); do
    original=$(ls -l $d | cut -f 5 -d' ')
    compressed=$(python3 ../main.py $d ../models/$d.pickle)
    echo ""
    echo -n "CO-net $d: "
    printf %.2f%%\\n $(echo "100-100*$compressed/$original" | bc -l)
    for a in $(ls $d.*); do
        compressed=$(ls -l $a | cut -f 5 -d' ')
        echo -n "$a: "
        printf %.2f%%\\n $(echo "100-100*$compressed/$original" | bc -l)
    done
done
