# Alpha Finder

## 项目背景
- 股票投资分析工具，目标是提升台股与美股中长期投资的报酬率
- 透过基本面筛选 + 回测验证，找出具有超额报酬（Alpha）的标的

## 技术栈
- 语言：Python
- 数据来源：yfinance（美股）、FinMind / twstock（台股）
- 数据处理：pandas, numpy
- 回测：backtrader
- 可视化：matplotlib, plotly
- Dashboard：Streamlit（后续开发）
- 通知：LINE Notify / Email（后续开发）

## 开发阶段

### 第一阶段：数据收集
- [ ] 台股数据抓取（股价、财报）
- [ ] 美股数据抓取（股价、财报）

### 第二阶段：基本面筛选器
- [ ] 自定义筛选条件（ROE、PE、殖利率、营收成长等）
- [ ] 自动产出候选标的清单

### 第三阶段：回测系统
- [ ] 定义交易策略
- [ ] 用历史数据验证策略绩效
- [ ] 产出报酬率、最大回撤、夏普比率等指标

### 第四阶段：通知与可视化（后续）
- [ ] Streamlit Dashboard
- [ ] LINE / Email 通知

## 项目结构
```
src/
├── data/        # 数据收集模块
├── screener/    # 基本面筛选器
├── backtest/    # 回测系统
├── notify/      # 通知模块
└── dashboard/   # 可视化仪表板
```
