"""sc-githooks - Pre-receive hook routines

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

from fileinput import input
from sys import stdout, stderr
from traceback import print_exc

from githooks.base_check import CheckState, prepare_checks, BaseCheck
from githooks.checks import checks
from githooks.config import config
from githooks.git import Commit
from githooks.utils import iter_buffer


class Runner(object):
    def __init__(self):
        self.checked_commit_ids = set()
        self.changed_file_checks = dict()

    def run(self):
        # check whether commit check is enabled
        commit_check_is_enabled = False
        try:
            commit_check_is_enabled = config.get("commit_check.enabled")
        except:
            pass
        if not commit_check_is_enabled:
            return CheckState.DONE

        state = CheckState.NEW

        # We are buffering the checks to let them run parallel in
        # the background.  Parallelization only applies to the CheckCommands.
        # It has no overhead, because we have to run those commands the same
        # way externally, anyway.  We only have a limit to avoid consuming
        # too many processes.
        # sc: add DEV_MODE
        dev_mode = False
        try:
            dev_mode = config.get("dev.dev_mode")
        except:
            pass
        if dev_mode:
            for check in self.expand_checks(checks):
                check.print_problems()
                assert check.state >= CheckState.DONE
                state = max(state, check.state)
        else:
            for check in iter_buffer(self.expand_checks(checks), 16):
                check.print_problems()
                assert check.state >= CheckState.DONE
                state = max(state, check.state)
        return state

    def expand_checks(self, checks):
        next_checks = []
        for check in prepare_checks(checks, None, next_checks):
            yield check

        for line in input():
            for check in self.expand_checks_to_input(next_checks, line):
                yield check

    def expand_checks_to_input(self, checks, line):
        line_split = line.split()
        ref_path_split = line_split[2].split('/', 2)
        if ref_path_split[0] != 'refs' or len(ref_path_split) != 3:
            # We have no idea what this is.
            return

        commit = Commit(line_split[1])
        if not commit:
            # This is a deletion.  We don't check anything on deletes.
            return

        if ref_path_split[1] == 'heads':
            name = line_split[2]
            for check in self.expand_checks_to_branch(checks, commit, name):
                yield check
        elif ref_path_split[1] == 'tags':
            for check in self.expand_checks_to_commit(checks, commit):
                yield check

    def expand_checks_to_branch(self, checks, commit, name):
        commit_list = commit.get_new_commit_list(name)

        # Appending the actual commit on the list to the new ones makes
        # testing easier.
        if commit not in commit_list:
            commit_list.append(commit)

        for check in self.expand_checks_to_commit_list(checks, commit_list):
            yield check

    def expand_checks_to_commit_list(self, checks, commit_list):
        next_checks = []
        for check in prepare_checks(checks, commit_list, next_checks):
            yield check

        for commit in commit_list:
            if commit.commit_id not in self.checked_commit_ids:
                for check in self.expand_checks_to_commit(next_checks, commit):
                    yield check
                self.checked_commit_ids.add(commit.commit_id)

    def expand_checks_to_commit(self, checks, commit):
        next_checks = []
        for check in prepare_checks(checks, commit, next_checks):
            yield check

        for changed_file in commit.get_changed_files():
            for check in self.expand_checks_to_file(next_checks, changed_file):
                yield check

    def expand_checks_to_file(self, checks, changed_file):
        # We first need to wait for the previous checks on the same file
        # to finish.  If one of them failed already, we don't bother checking
        # the same file again.  The committer should return back to her
        # commit she broke the file.  It makes too much noise to complain
        # about the same file on multiple commits.
        previous_checks = self.changed_file_checks.setdefault(
            changed_file.path, []
        )
        for check in previous_checks:
            assert check.state >= CheckState.CLONED
            # Wait for the check to run
            while check.state < CheckState.DONE:
                yield None
            if check.state >= CheckState.FAILED:
                return

        for check in prepare_checks(checks, changed_file):
            yield check
            previous_checks.append(check)


def main():
    try:
        state = Runner().run()
    except Exception as e:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        stdout.flush()
        print(file=stderr)
        print('{} An error occurred: {}'.format(BaseCheck.ERROR_MSG_PREFIX, e), file=stderr)
        print_exc()
        return 1
    else:
        if state >= CheckState.FAILED:
            return 1

    return 0
