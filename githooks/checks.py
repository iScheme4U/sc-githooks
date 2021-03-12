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

checks = []  # type: list

# # Commit list checks
# # 检查多个提交的提交标题是否重复
# checks.append(CheckDuplicateCommitSummaries())
# # 检查合并提交
# checks.append(CheckMisleadingMergeCommit())
# # 检查时间标签信息
# checks.append(CheckTimestamps())
# # 检查提交者信息
# checks.append(CheckContributors())

# Commit checks
# 提交消息（包含标题）检查
checks.append(CheckCommitMessage())
# 提交标题检查
checks.append(CheckCommitSummary())
# # 文件路径检查
# checks.append(CheckChangedFilePaths())

# 检查二进制文件
checks.append(CheckBinaryFiles())

# 检查文件后缀名
checks.append(CommittedFileExtensionCheck())

# Commit file size check
checks.append(CommittedFileSizeCheck())
