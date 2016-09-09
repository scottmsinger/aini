#
# old school hacky workaround to get aini vars in a bash script
#   without having to run everything through python, which, is
#   sometimes such a pain in the ass.
#

# run aini_env.py to spit out the current aini env as a=b value pairs
aini_vars=( $(~/bin/aini_env.py) )

# loop over the array and simply eval it to set the values
for av in "${aini_vars[@]}"
do
    eval $av
done

# hackey - yes, but I like it too.
