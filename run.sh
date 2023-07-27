#!/bin/sh

cd datasets
rm *.csv.*

# compress
for d in $(ls *.csv); do
    echo "Compressing $d..."
    gzip --best -k $d > /dev/null # deflate
    bzip2 --best -k $d > /dev/null # bzip2
    lzma --best -k $d > /dev/null # LZMA
    zstd --best -k $d 2> /dev/null # zstd
    lz4 --best -k $d $d.l4 2> /dev/null # LZ4
    7z a -m0=PPMd -mx=9 $d.ppmd $d > /dev/null # PPMd
    brotli --best -k $d > /dev/null # brotli
    zpaq -m5 add $d.zpaq $d 1> /dev/null 2> /dev/null # zpaq
    mscompress $d > /dev/null # LZ77
    mv "$d"_ $d.lz77
    # snzip -k $d # snappy, https://github.com/kubo/snzip
done

echo ""
echo -n "    Compression rate:"
# compute compression rate
for d in $(ls *.csv); do
    original=$(ls -l $d | cut -f 5 -d' ')
    echo ""

    echo -n "CO-net $d: "
    compressed=$(python3 ../main.py $d ../models/$d.pickle)
    printf %.2f%%\\n $(echo "100-100*$compressed/$original" | bc -l)

    echo -n "Separable CO-net $d: "
    compressed=$(python3 ../main.py $d ../models/"$d"_sep.pickle)
    printf %.2f%%\\n $(echo "100-100*$compressed/$original" | bc -l)

    echo -n "Entropy coding of $d: "
    entropy=$(ent $d -t | grep "^1" | cut -d"," -f 3)
    printf %.2f%%\\n $(echo "100-100*$entropy/8" | bc -l)

    for a in $(ls $d.*); do
        compressed=$(ls -l $a | cut -f 5 -d' ')
        echo -n "$a: "
        printf %.2f%%\\n $(echo "100-100*$compressed/$original" | bc -l)
    done
done
