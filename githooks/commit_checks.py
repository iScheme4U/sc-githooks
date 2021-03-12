"""sc-githooks - Checks on Git commits

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

from githooks.config import config
from githooks.base_check import BaseCheck, Severity
from githooks.git import Commit


class CommitCheck(BaseCheck):
    """Parent class for all single commit checks"""
    commit = None

    def prepare(self, obj):
        new = super(CommitCheck, self).prepare(obj)
        if not new or not isinstance(obj, Commit):
            return new

        new = new.clone()
        new.commit = obj
        return new

    def __str__(self):
        return '{} 位于提交 {}'.format(type(self).__name__, self.commit)


class CheckCommitMessage(CommitCheck):
    """提交消息（包含标题）检查
    检查长度、空行等问题"""

    def get_problems(self):
        for line_id, line in enumerate(self.commit.get_message_lines()):
            if line_id == 0:
                continue
            elif line_id == 1:
                if line.strip():
                    yield Severity.ERROR, '第二行应为空行'
            else:
                if line.startswith('    ') or line.startswith('>'):
                    continue

            if line:
                for problem in self.get_line_problems(line_id + 1, line):
                    yield problem

    def get_line_problems(self, line_number, line):
        # if line.rstrip() != line:
        #     line = line.rstrip()
        #     yield (
        #         Severity.ERROR,
        #         '行 {}: 右边不应该包含空格字符'.format(line_number)
        #     )
        #
        # if line.lstrip() != line:
        #     line = line.lstrip()
        #     yield (
        #         Severity.WARNING,
        #         '行 {}: 左边包含空格字符'.format(line_number)
        #     )
        if len(line) > config.get("commit_check.commit_line_max_length"):
            yield (
                Severity.WARNING,
                '行 {}: 超过 {} 字符'.format(line_number, config.get("commit_check.commit_line_max_length"))
            )


class CheckCommitSummary(CommitCheck):
    """提交标题检查
    检查标题的标记、回退等问题"""
    commit_tags = {
        'BREAKING',
        'BUGFIX',
        'CLEANUP',
        'FEATURE',
        'HOTFIX',
        'MESS',
        'MIGRATE',
        'REFACTORING',
        'REVIEW',
        'SECURITY',
        'STYLE',
        'TASK',
        'TEMP',
        'WIP',
        '!!',
    }

    def get_problems(self):
        tags, rest = self.commit.parse_tags()
        # if rest.startswith('['):
        #     yield Severity.WARNING, '未结束的提交标记'
        # if tags:
        #     for problem in self.get_commit_tag_problems(tags, rest):
        #         yield problem
        #     rest = rest[1:]
        #
        # if rest.startswith('Revert'):
        #     for problem in self.get_revert_commit_problems(rest):
        #         yield problem
        #     return

        for problem in self.get_summary_problems(rest):
            yield problem

    # def get_revert_commit_problems(self, rest):
    #     rest = rest[len('Revert'):]
    #     if not rest.startswith(' "') or not rest.endswith('"'):
    #         yield Severity.WARNING, '回退的提交消息格式不合法'
    #
    # def get_commit_tag_problems(self, tags, rest):
    #     used_tags = []
    #     for tag in tags:
    #         tag_upper = tag.upper()
    #         if tag != tag_upper:
    #             yield (
    #                 Severity.ERROR,
    #                 '提交标记 [{}] 不是大写字符'.format(tag)
    #             )
    #         if tag_upper not in CheckCommitSummary.commit_tags:
    #             yield (
    #                 Severity.WARNING,
    #                 '提交标记 [{}] 不在清单中 {}'.format(
    #                     tag, ', '.join(
    #                         '[{}]'.format(t)
    #                         for t in CheckCommitSummary.commit_tags
    #                     )
    #                 )
    #             )
    #         if tag_upper in used_tags:
    #             yield Severity.ERROR, '重复的提交标记 [{}]'.format(tag)
    #         used_tags.append(tag_upper)
    #
    #     if not rest.startswith(' '):
    #         yield Severity.WARNING, '没有使用空格将提交标记与其他内容分开'

    def get_summary_problems(self, rest):
        if not rest:
            yield Severity.ERROR, '无提交标题'
            return

        rest_len = len(rest)
        if rest_len > config.get("commit_check.commit_line_max_length"):
            yield Severity.ERROR, "提交标题不能超过 {} 个字符".format(config.get("commit_check.commit_line_max_length"))
        elif rest_len > config.get("commit_check.commit_summary_max_length"):
            yield Severity.WARNING, "提交标题超过了 {} 个字符".format(config.get("commit_check.commit_summary_max_length"))

        # if '  ' in rest:
        #     yield Severity.WARNING, '存在多个空格字符'

        category_index = rest[:24].find(': ')
        rest_index = category_index + len(': ')
        if category_index >= 0 and len(rest) > rest_index:
            # for problem in self.get_category_problems(rest[:category_index]):
            #     yield problem
            rest = rest[rest_index:]

        for problem in self.get_title_problems(rest):
            yield problem
    #
    # def get_category_problems(self, category):
    #     if not category[0].isalpha():
    #         yield Severity.WARNING, '提交类型以非字母字符开头'
    #     if category.lower() != category:
    #         yield Severity.WARNING, '提交类型包含大写字符'
    #     if category.rstrip() != category:
    #         yield Severity.WARNING, '提交类型右边包含空格字符'

    def get_title_problems(self, rest):
        if not rest:
            yield Severity.ERROR, '无提交标题'
            return
        #
        # first_letter = rest[0]
        # if not first_letter.isalpha():
        #     yield Severity.WARNING, '提交标题以非字母开始'
        # elif first_letter.upper() != first_letter:
        #     yield Severity.WARNING, '提交标题首字母不是大写'
        #
        # if rest.endswith('.'):
        #     yield Severity.WARNING, "提交标题以'.'字符结尾"
        #
        # first_word = rest.split(' ', 1)[0]
        # if first_word.endswith('ed'):
        #     yield Severity.WARNING, '提交标题使用的过去式'
        # if first_word.endswith('ing'):
        #     yield Severity.WARNING, '提交标题使用的进行时'


class CheckChangedFilePaths(CommitCheck):
    """Check file names and directories on a single commit"""

    def get_problems(self):
        for changed_file in self.commit.get_changed_files():
            extension = changed_file.get_extension()
            if (
                    extension in ('pp', 'py', 'sh') and
                    changed_file.path != changed_file.path.lower()
            ):
                yield Severity.WARNING, '{} 文件名使用了大写字母'.format(changed_file)


class CheckBinaryFiles(CommitCheck):
    """Check whether binary files exists on a single commit"""

    def get_problems(self):
        for binary_file in self.commit.get_binary_files():
            yield Severity.WARNING, '文件 {} 是二进制文件'.format(binary_file)
