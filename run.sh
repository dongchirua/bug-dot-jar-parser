#!/bin/bash
#bash run.sh ~/workplace/bugs-dot-jar ~/Desktop/out

current_folder=`pwd`
python_script="${current_folder}/extract_bug_dot_jar.py"
echo "python script location: $python_script"


bug_dot_jar_location=$1
echo "bug.jar location: $bug_dot_jar_location"
echo "save place: $2"

total_bugs=0

for d in $bug_dot_jar_location*/* ; do
    [ -d "${d}" ] || continue # if not a directory, skip
    cd "$d"
    git stash
    git clean -fd

    cnt=0
    for i in `(git branch -a | grep remotes/origin/bugs-dot-jar_)`; do
        cnt=$((cnt+1))
    done
    n_branches="$cnt"
    echo $d
    for branch in `(git branch -a | grep remotes/origin/bugs-dot-jar_)`; do
        branch_name=$(echo ${branch} | cut -d'/' -f 3);
        # echo $branch_name
        # git branch -d ${branch_name};
        git checkout ${branch_name} -q;
        git stash
        git clean -fd
        python $python_script \
                --diff_src='./.bugs-dot-jar/developer-patch.diff' \
                --single_desc="$2" \
                --multi_desc="$2";
    done | pv -l -s "$n_branches" > /dev/null

    total_bugs=$((total_bugs+cnt))
done

echo "done! with $total_bugs bugs"




