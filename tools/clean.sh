# tools/clean.sh
#
# clean projects directory.
#
# Author: Jiajun Liu <jiajun@unitedstack.com>
#


# Sanitize language settings to avoid targetss bailing out
# with "unsupported locale setting" errors.
unset LANG
unset LANGUAGE
LC_ALL=C
export LC_ALL

# Make sure umask is sane
umask 022

# Keep track of the top directory
CURDIR=$(cd $(dirname "$0") && pwd)
TOPDIR=$(dirname "${CURDIR}")

usage () {
    echo "USAGE: $0 <project|all> <src|rpm|all>"
    echo ""
    exit
}


is_valid_targets() {
    local targets=$1
    local avalible_targets=("src" "rpm" "all")

    for val in ${avalible_targets[@]}; do
        if [[ "${val}" == "${targets}" ]]; then
            return 0
        fi
    done
    return 1
}


is_valid_project() {
    local project=$1

    if [[ "all" == "${project}" ]]; then
        return 0
    fi

    local avalible_projects=( $(ls ${TOPDIR}/projects) )
    for val in ${avalible_projects[@]}; do
        if [[ "${val}" == "${project}" ]]; then
            return 0
        fi
    done
    return 1
}


clean_rpm() {
    local project=$1

    if [ "all" = "${project}" ]; then
        projectdir="${TOPDIR}/projects"
    else
        projectdir="${TOPDIR}/projects/${project}"
    fi
    pushd "${projectdir}" > /dev/null
    find -name "*.rpm" -delete
    popd > /dev/null
}


clean_src() {
    local project=$1

    if [ "all" = "${project}" ]; then
        for project in $(ls "${TOPDIR}/projects"); do
            rm -fr "${TOPDIR}/projects/${project}/SRC"
        done
    else
        rm -fr "${TOPDIR}/projects/${project}/SRC"
    fi
}


if [ $# -ne 2 ]; then
    usage
fi

project=$1
targets=$2

is_valid_project ${project} || usage
is_valid_targets ${targets} || usage


if [ "rpm" = "${targets}" ]; then
    clean_rpm "${project}"
elif [ "src" = "${targets}" ]; then
    clean_src "${project}"
else
    clean_rpm "${project}"
    clean_src "${project}"
fi
