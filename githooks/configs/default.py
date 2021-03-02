DEFAULT_CONFIG = {
    # 是否开发模式
    "dev": {
        "dev_mode": False,
    },
    "commit_check": {
        # 是否启动提交检查
        "enabled": True,
        # 提交标题行最大长度
        "commit_summary_max_length": 50,
        # 提交详细行最大行长度
        "commit_line_max_length": 80,

        # 二进制文件黑名单（逗号分隔的后缀名清单，无需带.，通过后缀名控制）
        "binary_file_illegal_suffixes": "jar",
        # 二进制文件白名单（逗号分隔的区分大小写的文件名列表，这些二进制文件允许提交）
        "legal_binary_filenames": "gradle-wrapper.jar,maven-wrapper.jar",

        # 提交文件最大大小(5MB)
        "commit_file_max_size": 5242880,
    }
}
