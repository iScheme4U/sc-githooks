.. image:: https://badge.fury.io/py/sc-githooks.svg
    :target: https://badge.fury.io/py/sc-githooks
.. image:: https://img.shields.io/pypi/pyversions/sc-githooks
    :alt: PyPI - Python Version

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

If you want all projects to be checked, then you need to do following steps:

    #. On the GitLab server, navigate to the configured custom hook directory. The default is in the gitlab-shell directory.

    #. The gitlab-shell hook directory for Omnibus installation is usually /opt/gitlab/embedded/service/gitlab-shell/hooks.

    #. Create a new directory in this location. Depending on your hook, it will be either a pre-receive.d, post-receive.d,
       or update.d directory.

    #. Inside this new directory, add your hook like this::

        cd /opt/gitlab/embedded/service/gitlab-shell/hooks
        mkdir pre-receive.d
        cd pre-receive.d
        ln -s /usr/local/bin/sc-pre-receive pre-receive

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

First, make sure /var/opt/sc directory exists, if not create this directory and make sure current user has the right
to create files in this directory.

You can copy `default.yml <https://github.com/Scott-Lau/sc-githooks/blob/master/githooks/tests/sample_config/default.yml>`_
to /var/opt/sc/.sc-githooks/production.yml to initialize the production configuration.

The default configuration file looks like this::

    dev:
      # Whether this program is running in development mode
      dev_mode: False

    commit_check:
      # Whether commit check is enabled
      enabled: True
      # The warning threshold of the length of commit summary
      commit_summary_max_length: 50
      # The threshold of the max length of commit summary and other commit line
      commit_line_max_length: 80

      # A list of illegal suffixes which cannot be committed to git repository
      binary_file_illegal_suffixes: "jar"
      # A list of legal binary file names which can be committed to git repository
      legal_binary_filenames: "gradle-wrapper.jar,maven-wrapper.jar"

      # The max size of a file that can be committed to git repository
      commit_file_max_size: 5242880

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

* `sc-config <https://github.com/Scott-Lau/sc-config>`_ >= 0.0.3


Testing
-------

I found it useful to check what the script would have complained if it had
been active on different Git repositories.  You can run a command like this
to test this inside a Git repository against last 50 commits::

    git log --reverse --oneline HEAD~50..HEAD |
        sed 's:\([^ ]*\) .*:\1 \1 refs/heads/master:' |
        python ../sc-githooks/sc-pre-receive

License
-------

The script is released under the MIT License.  The MIT License is registered
with and approved by the Open Source Initiative [1]_.

.. [1] https://opensource.org/licenses/MIT
