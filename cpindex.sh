# script to copy index.php file into the remote directory

path_to_output=$1
echo "Copying index.php to ${path_to_output} directory resursively..."
for d in $( find $path_to_output/* -type d ); do
    if [ -d "$d" ]
    then
        if [ -f "$d/index.php" ]
        then
            echo "index.php exists in $d"
        else
            cp index.php $d
        fi
    fi
done
