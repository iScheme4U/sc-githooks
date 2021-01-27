"""sc-githooks - Checks on files committed to Git

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

from githooks.base_check import BaseCheck, Severity
from githooks.config import config
from githooks.git import CommittedFile


class CommittedFileCheck(BaseCheck):
    """Parent class for checks on a single committed file

    To check the files, we have to clone ourselves when we are being prepared
    for the CommittedFile.  The subclasses has additional logic on those
    to filter out themselves for some cases.
    """
    committed_file = None

    def prepare(self, obj):
        new = super(CommittedFileCheck, self).prepare(obj)
        if not new or not isinstance(obj, CommittedFile):
            return new

        new = new.clone()
        new.committed_file = obj
        return new

    def __str__(self):
        return '{} on {}'.format(type(self).__name__, self.committed_file)


class CommittedFileSizeCheck(CommittedFileCheck):
    """Special check for committed file size"""

    def get_problems(self):
        if self.committed_file.get_file_size() >= config.get("commit_check.commit_file_max_size"):
            yield (
                Severity.ERROR,
                '提交 {} 的文件 {} 大小超过 {}, 即 {} MB'
                    .format(self.committed_file.commit, self.committed_file.path,
                            config.get("commit_check.commit_file_max_size"),
                            config.get("commit_check.commit_file_max_size") / 1024 / 1024)
            )


class CommittedFileExtensionCheck(CommittedFileCheck):
    """Special check for committed file extension"""

    def get_problems(self):
        illegal_suffixes = config.get("commit_check.binary_file_illegal_suffixes")
        illegal_suffixes_list = illegal_suffixes.split(",")
        legal_binary_filenames = config.get("commit_check.legal_binary_filenames")
        legal_binary_filenames_list = legal_binary_filenames.split(",")
        filename = self.committed_file.get_filename()
        if filename in legal_binary_filenames_list:
            return
        extension = self.committed_file.get_extension()
        if extension in illegal_suffixes_list:
            yield (
                Severity.ERROR,
                '提交 {} 的文件 {} 在不允许的提交文件后缀名清单中 {}'
                    .format(self.committed_file.commit, self.committed_file.path,
                            illegal_suffixes_list)
            )
