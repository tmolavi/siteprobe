# First Contribution Guide: SiteProbe

Welcome to SiteProbe! We welcome contributions to our crawler, diagnostic rule checks, and safe autofix generators.

---

## ⚡ 5-Step Contributor Journey

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/tmolavi/siteprobe.git
   cd siteprobe
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

2. **Run Tests & Demo**:
   ```bash
   PYTHONPATH=src pytest tests/ -v
   PYTHONPATH=src python examples/public_demo/run_demo.py
   ```

3. **Open Issue / Discussion**: Check [GitHub Discussions](https://github.com/tmolavi/siteprobe/discussions).
4. **Implement Changes**: Follow deterministic autofix safety rules.
5. **Submit Pull Request**: Open a PR with tests covering any new crawl check or fix generator.
