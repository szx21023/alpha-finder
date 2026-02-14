# Alpha Finder

股票投资分析工具，透过基本面筛选与回测验证，寻找具有超额报酬（Alpha）的台股与美股标的。

## 功能

- **数据收集**：自动抓取台股与美股的股价、财报数据
- **基本面筛选**：根据 ROE、PE、殖利率、营收成长等指标筛选标的
- **回测系统**：用历史数据验证交易策略的绩效
- **通知提醒**：符合条件的标的自动通知（开发中）
- **可视化**：Streamlit Dashboard 展示分析结果（开发中）

## 安装

```bash
# Clone 项目
git clone git@github.com:szx21023/alpha-finder.git
cd alpha-finder

# 建立虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

## 项目结构

```
src/
├── data/        # 数据收集模块
├── screener/    # 基本面筛选器
├── backtest/    # 回测系统
├── notify/      # 通知模块
└── dashboard/   # 可视化仪表板
```

## 配置

编辑 `config/settings.yaml` 自定义筛选条件与回测参数。
