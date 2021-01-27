Git Pre-Receive Hook to Validate Commits
========================================

This project provides a Git pre-receive hook to validate pushed commits on
the Git server side.  The hook avoids all issues by rejecting any commit
not matching the rules to get in to the repository in the first place.


Installation
------------

It is possible to install the tool with `pip`::

    pip install sc-githooks

Link the `script <sc-pre-receive>`_ to ``hooks/pre-receive`` on you Git
repositories on your Git server::

    ln -s sc-pre-receive /home/git/repositories/myproject.git/hooks/pre-receive


Features
--------

* Validate received commits one by one not just the last one
* Only validate added or modified files on the commits
* Report all problems before failing
* Check for duplicate commit summaries
* Check for misleading merge commits
* Validate committer and author timestamps
* Validate committer and author names and email addresses
* Check commit message best practices (80 lines, first line summary...)
* Check commit summary formatting
* Validate commit tags against a list ``[BUGFIX]``, ``[FEATURE]``, ``[WIP]``...
* Check for changed file paths
* Accept commits tagged as ``[HOTFIX]``, ``[MESS]``, ``[TEMP]``, or ``[WIP]``
  with issues
* Check binary files
* Check file size
* Check file extensions

Here is an example problem output::

    === CheckDuplicateCommitSummaries on CommitList ===
    ERROR: summary "Add nagios check for early expiration of licenses" duplicated 2 times

    === CheckCommitSummary on 31d0f6b ===
    WARNING: summary longer than 72 characters

    === CheckCommitSummary on 6bded65 ===
    WARNING: past tense used on summary

    === CheckCommitMessage on 6fdbc00 ===
    WARNING: line 7 is longer than 80
    WARNING: line 9 is longer than 80


Configuration
-------------

See `config.py <githooks/config.py>`_ for more information.
    * DEV_MODE
        * Whether this program is running in development mode
    * COMMIT_SUMMARY_MAX_LENGTH
        * The warning threshold of the length of commit summary
    * COMMIT_LINE_MAX_LENGTH
        * The threshold of the max length of commit summary and other commit line
    * BINARY_FILE_ILLEGAL_SUFFIXES
        * A list of illegal suffixes which cannot be committed to git repository
    * LEGAL_BINARY_FILENAMES
        * A list of legal binary file names which can be committed to git repository
    * COMMIT_FILE_MAX_SIZE
        * The max size of a file that can be committed to git repository


Pros and Cons of Pre-receive Hook
---------------------------------

Continuous Integration Server
    A continuous integration server can run such checks with the many other
    things it is doing.  Moving this job from it has many benefits:

    * Synchronous feedback
    * More efficient
    * Disallow any commit violating the rules

Pre-commit Hook
    Even though, pre-receive hook gives later feedback than pre-commit hook,
    it has many advantages over it:

    * No client side configuration
    * Plugins has to be installed only once to the Git server
    * Everybody gets the same checks
    * Enforcement, nobody can skip the checks
    * Commit checking (pre-commit hook only gets what is changed in the commit)

IDE Integration
    The same advantages compared to pre-commit hooks applies to IDE
    integration.  Though, IDE integration gives much sooner and nicer feedback,
    so it is still a good idea, even with the pre-receive hook.


Dependencies
------------

The script has no dependencies on Python 3.4 or above.  The script executes
the validation commands using the shell.  The necessary ones for checked
repositories need to be installed separately.  See the complete list of
commands on the `config.py <githooks/config.py>`_.  The commands which are not
available on the ``PATH`` is not going to be used.


Testing
-------

I found it useful to check what the script would have complained if it had
been active on different Git repositories.  You can run a command like this
to test this inside a Git repository against last 50 commits::

    git log --reverse --oneline HEAD~50..HEAD |
        sed 's:\([^ ]*\) .*:\1 \1 refs/heads/master:' |
        python ../sc-githooks/sc-pre-receive


Changes
-------

Version 0.1
    * Initial version check commit
    * Add binary file check
    * Add file extensions check
    * Add file size check

Version 0.1.1
    * Unique source of version

License
-------

The script is released under the MIT License.  The MIT License is registered
with and approved by the Open Source Initiative [1]_.

.. [1] https://opensource.org/licenses/MIT
