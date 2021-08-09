ENVIRONMENT="$1"

[ -z "$ENVIRONMENT" ] && ENVIRONMENT='local'

if "$ENVIRONMENT" == 'local'
then
  echo "Building module in place"
  python3 "./setup.py" build_ext --inplace
else
  echo "Building module"
  python3 "./setup.py" build_ext
fi

echo "Done building Treeshake. Check the output folders."