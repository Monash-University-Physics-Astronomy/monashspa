# Contributing
We welcome improvements to monashspa!

Improvements made during semesters must not break existing code (only backwards compatible feature additions and bug fixes will be accepted)

At the end of semester 2 each year, the entire repository will be archived into a new module, named after the year, to allow students to execute code from previous years without running into errors (this will require them to update their imports from `monashspa.PHS1011` to `monashspa.2019.PHS1011` for example).

# Process for contributing
1. [Fork](https://bitbucket.org/monashuniversityphysics/monashspa/fork) the repository on bitbucket (this requires a bitbucket account).
4. Make the modifications. You may wish to clone your fork locally using a mercurial client such as TortoiseHg or MacHG, make the edits there, and then commit and push the changes to your fork.
    * For small modifications, commit to the default branch in your forked repository
    * For large changes (such as new features) commit your changes to a new branch in your forked repository
5. Test your changes and make sure they are complete and you have not introduced any regressions (ensure your changes pass all automated tests we provide in the `monashspa/tests` folder). You may also want to add new tests that cover the changes you have made.
6. Update the documentation in the "docs" folder to make it consistent with your changes.
8. Using the bitbucket web interface for your forked repository, make a pull-request to the main monashspa repository. 
8. We will review your pull-request (you may wish to directly email the Monash admin staff maintaining the repository to speed this up), and may request changes to your code if it breaks compatibility with other units.
9. Once the pull-request has been reviewed, we will merge in your changes and push a new version to PyPi so that students can upgrade by running the command `pip install -U monashspa`.
