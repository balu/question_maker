cd $1
yamlfile=$1.yaml
shift
python ../q.py $yamlfile "$@"
touch q.log
for i in *.tex
do
    xelatex -pdf $i > /dev/null 2>&1
    xelatex -pdf $i > /dev/null 2>&1
    echo $i > /dev/stderr
done

gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=qp.pdf -dBATCH -c "[ /Title ($yamlfile) /DOCINFO pdfmark" -f *[A-Z].pdf > /dev/null 2>&1
rm *.log *.aux *.tex
rm *[A-Z].pdf
cd ..
