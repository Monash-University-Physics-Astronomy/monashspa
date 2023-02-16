# Release
A new release can only be made by GitHub users that are authenticated with write access to the main repository (so not a fork).

# Process for making a release
1. Make sure that all changes to the code, the documentation and tests are checked into the HEAD of the master branch.
2. In `setup.py` bump the version number. It has the format `X.Y.Z`. For bug fixes or tiny tweaks, increment `Z`. For a new feature that has no effect on other code, increment `Y` and reset `Z` to zero. For a change that will require changes to student code used in all units, discuss will all involved parties first, and then increment `X` and reset `Y` and `Z`.
3. Go to the [release page in the GitHub repo](https://github.com/Monash-University-Physics-Astronomy/monashspa/releases) and select `Draft a new release`. Explain what is new in the webform, and give it the same tag `X.Y.Z` that you just updated `setup.py` with.
4. Select `publish release` on the page. If everything goes well, the release will be pushed to [PyPi](https://pypi.org/project/monashspa/) and you should see the new release number.
