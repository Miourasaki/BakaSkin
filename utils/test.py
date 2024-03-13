def calculate_hash(string):
    # 使用Python内置的哈希函数计算哈希值
    hash_value = hash(string)

    # 将哈希值与1取余，得到最后的结果
    result = hash_value % 2

    return result

# 示例用法
