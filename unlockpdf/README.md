## 解锁PDF

> 本仓库是基于某个大佬的代码整理的

可以给一些没密码但无法编辑的pdf进行解锁。

做了简单的gui，编译成exe在`Releases`可以下载。

### 使用说明

程序会按照文件夹将pdf分组解锁。


#### 操作流程

1. 选择`documents`作为根目录。
2. 点击开始。
3. 输出文件。

#### 示例

需要合并的内容如下。

```sh
├── documents
│   ├── reports
│   │   ├── financial-summary-2023.pdf
│   │   ├── market-analysis-q4.pdf
│   │   └── yearly-report-archive
│   │       ├── report-2020.pdf
│   │       ├── report-2021.pdf
│   │       └── report-2022.pdf
│   ├── guides
│   │   ├── user-guide.pdf
│   │   ├── setup-instructions.pdf
│   │   └── advanced-tips.pdf
│   └── templates
│       ├── invoice-template.pdf
│       ├── proposal-template.pdf
│       ├── contract-template.pdf
│       └── checklist-template.pdf
```

输出：

```sh
├── documents
│   ├── yearly-report-archive
│   │   ├── report-2020.pdf
│   │   ├── report-2021.pdf
│   │   └── report-2022.pdf
│   ├── reports
│   │   ├── financial-summary-2023.pdf
│   │   └── market-analysis-q4.pdf
│   ├── guides
│   │   ├── user-guide.pdf
│   │   ├── setup-instructions.pdf
│   │   └── advanced-tips.pdf
│   └── templates
│       ├── invoice-template.pdf
│       ├── proposal-template.pdf
│       ├── contract-template.pdf
│       └── checklist-template.pdf
```
**其中，`out`文件夹为输出结果。**