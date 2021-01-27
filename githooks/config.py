"""sc-githooks - Configurations

Copyright (c) 2021 Scott Lau
"""

# 是否开发模式
DEV_MODE = False
# DEV_MODE = True

# 提交标题行最大长度
COMMIT_SUMMARY_MAX_LENGTH = 50
# 提交详细行最大行长度
COMMIT_LINE_MAX_LENGTH = 80

# 二进制文件黑名单（逗号分隔的后缀名清单，无需带.，通过后缀名控制）
BINARY_FILE_ILLEGAL_SUFFIXES = "jar"
# 二进制文件白名单（逗号分隔的区分大小写的文件名列表，这些二进制文件允许提交）
LEGAL_BINARY_FILENAMES = "gradle-wrapper.jar,maven-wrapper.jar"

# 提交文件最大大小(5MB)
COMMIT_FILE_MAX_SIZE = 5242880
