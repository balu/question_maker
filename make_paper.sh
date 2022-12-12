cd $1
python ../q.py $1.yaml
touch q.log
for i in *.tex
do
    xelatex -pdf $i > /dev/null 2>&1
    xelatex -pdf $i > /dev/null 2>&1
    echo $i > /dev/stderr
done

gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=qp.pdf -dBATCH -c "[ /Title ($1) /DOCINFO pdfmark" -f *[A-Z].pdf > /dev/null 2>&1
rm *.log *.aux *.tex
rm *[A-Z].pdf
cd ..
