#!/bin/bash

# Build the executable
poetry run pyinstaller src/clustify/cli/run.py --workpath _build/ -F -n "clustify"

# Create run.sh script
# TODO: HACK but does what it needs to for now. Better to use a template file.
printf "#!/bin/bash\n\n" > run.sh
printf "cd $(pwd)\n" >> run.sh
printf "# Read secret environment variables from .env file\n" >> run.sh
printf "source .env\n" >> run.sh

printf "# Check file dist/clustify exists\n" >> run.sh
printf "if [ ! -f dist/clustify ]; then\n" >> run.sh
printf "    echo 'File dist/clustify does not exist. Run build.sh first.'\n" >> run.sh
printf "    exit 1\n" >> run.sh
printf "fi\n" >> run.sh

printf "# Run the executable with all parameters passed to this script\n" >> run.sh
printf "./dist/clustify \"\$@\"" >> run.sh

chmod +x run.sh
