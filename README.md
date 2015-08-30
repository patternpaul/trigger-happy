# trigger-happy
When git reset --hard goes wrong and you want to recover those files

# what to do?

* put the trigger-happy.py file in the root of your Repo
* run git fsck --cache --unreachable $(git for-each-ref --format="%(objectname)") > derp
* run python trigger-happy.py

# notes
The scripts have lots of assumptions. Its assuming you are building a Lumen (or Laravel) php project. You can use this as an example for whatever you lost. You could just create random file names and then rename them.
