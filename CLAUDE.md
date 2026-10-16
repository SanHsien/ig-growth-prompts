# CLAUDE.md

規則的單一真相源是 [AGENTS.md](AGENTS.md)，先讀它。這裡只放專屬補充：

- 回覆一律用繁體中文，先結論後細節，不說客套話。
- 宣稱完成前附上 `pwsh -File tools/dev_check.ps1` 或 `python -m unittest discover -s tests -p "test_*.py" -v` 的實際輸出。
- Windows 11 原生環境，不用 POSIX 假設。
