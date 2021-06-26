for file in $( find rabbitai/translations/** );
do
  extension=${file##*.}
  filename="${file%.*}"
  if [ $extension == "po" ]
  then
    po2json --domain rabbitai --format jed1.x $file $filename.json
    ./rabbitai-frontend/node_modules/.bin/prettier --write $filename.json
  fi
done
