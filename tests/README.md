# 测试文件目录

本目录包含AutoSurvey项目的各种测试和示例文件。

## 目录内容

```
tests/
├── README.md                    # 本说明文件
├── test_paper_provider.py      # Paper Provider模块测试
└── use_lattereview_wrapper.py  # LatteReview包装器使用示例
```

## 文件说明

### 1. `test_paper_provider.py`
- **用途**: 测试Paper Provider模块的功能
- **功能**: 验证paper数据加载、处理和查询功能
- **使用方法**: 
  ```bash
  python tests/test_paper_provider.py
  ```

### 2. `use_lattereview_wrapper.py`
- **用途**: 展示如何使用LatteReview包装器
- **功能**: 演示LatteReview集成功能
- **使用方法**: 
  ```bash
  python tests/use_lattereview_wrapper.py
  ```

## 运行测试

### 环境要求
确保已安装所有必要的依赖：
```bash
pip install -r requirements.txt
```

### 运行所有测试
```bash
# 在项目根目录运行
python -m pytest tests/ -v

# 或者直接运行Python文件
python tests/test_paper_provider.py
python tests/use_lattereview_wrapper.py
```

## 测试注意事项

1. **数据文件**: 某些测试可能需要特定的数据文件，请确保相关文件存在
2. **API密钥**: 如果测试涉及外部API调用，请设置相应的环境变量
3. **输出目录**: 测试可能会生成输出文件，请检查`output/`目录

## 添加新测试

当添加新的测试文件时：
1. 将测试文件放在`tests/`目录中
2. 更新本README文件，说明新测试的用途和使用方法
3. 确保测试文件不包含敏感信息（如API密钥）

## 故障排除

如果测试失败：
1. 检查Python环境和依赖是否正确安装
2. 确认必要的数据文件是否存在
3. 查看错误信息，检查文件路径和配置
4. 参考主项目的README文件获取更多信息
