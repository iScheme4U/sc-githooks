"""sc-githooks - Configuration of the checks

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

from githooks.commit_checks import (
    CheckCommitMessage,
    CheckCommitSummary,
    CheckChangedFilePaths,
    CheckBinaryFiles,
)
from githooks.commit_list_checks import (
    CheckDuplicateCommitSummaries,
    CheckMisleadingMergeCommit,
    CheckTimestamps,
    CheckContributors,
)
from githooks.file_checks import (
    CommittedFileSizeCheck,
    CommittedFileExtensionCheck,
)

# 是否开发模式
DEV_MODE = False
# DEV_MODE = True

checks = []  # type: list

# Commit list checks
# 检查多个提交的提交标题是否重复
checks.append(CheckDuplicateCommitSummaries())
# 检查合并提交
checks.append(CheckMisleadingMergeCommit())
# 检查时间标签信息
checks.append(CheckTimestamps())
# 检查提交者信息
checks.append(CheckContributors())

# 提交标题行最大长度
COMMIT_SUMMARY_MAX_LENGTH = 50
# 提交详细行最大行长度
COMMIT_LINE_MAX_LENGTH = 80

# Commit checks
# 提交消息（包含标题）检查
checks.append(CheckCommitMessage())
# 提交标题检查
checks.append(CheckCommitSummary())
# 文件路径检查
checks.append(CheckChangedFilePaths())

# 检查二进制文件
checks.append(CheckBinaryFiles())

# 二进制文件黑名单（逗号分隔的后缀名清单，无需带.，通过后缀名控制）
BINARY_FILE_ILLEGAL_SUFFIXES = "jar"
# 二进制文件白名单（逗号分隔的区分大小写的文件名列表，这些二进制文件允许提交）
LEGAL_BINARY_FILENAMES = "gradle-wrapper.jar,maven-wrapper.jar"
# 检查文件后缀名
checks.append(CommittedFileExtensionCheck())

# 提交文件最大大小(5MB)
COMMIT_FILE_MAX_SIZE = 5242880

# Commit file size check
checks.append(CommittedFileSizeCheck())
