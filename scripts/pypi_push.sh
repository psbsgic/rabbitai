# Make sure you've followed the instructions on `RELEASING/README.md`
# and are on the correct branch
cd ${RABBITAI_REPO_DIR}
git branch
rm rabbitai/static/assets/*
cd rabbitai-frontend/
npm ci && npm run build
cd ../
echo "----------------------"
echo "Compiling translations"
echo "----------------------"
flask fab babel-compile --target rabbitai/translations
echo "----------------------"
echo "Creating distribution "
echo "----------------------"
python setup.py sdist
echo "RUN: twine upload dist/apache-rabbitai-${RABBITAI_VERSION}.tar.gz"
