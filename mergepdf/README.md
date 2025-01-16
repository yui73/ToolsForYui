## 合并PDF

*本仓库是基于某个大佬的代码整理修改的*

*哪位大佬等我想起来贴链接_(¦3」∠)_*

### 使用说明

程序会按照文件夹将pdf分组合并。

> 特别提示，加密文件需要输入密码解密并保存之后才可以进行合并。
> 如果文件没有密码，但显示无法合并，需要使用仓库内的另一个工具`unlockpdf`进行解锁后，再进行合并。

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
│   ├── out
│   │   ├── reports.pdf
│   │   ├── yearly-report-archive.pdf
│   │   ├── market-analysis-q4.pdf
│   │   ├── guides.pdf
│   │   └── templates.pdf
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
**其中，`out`文件夹为输出结果。**
