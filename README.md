# Magento E-commerce Test Automation Framework

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-latest-green.svg)](https://www.selenium.dev/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pytest](https://img.shields.io/badge/pytest-7.4.3-blue.svg)](https://docs.pytest.org/)

## 🎯 Project Overview

An enterprise-grade test automation framework designed for Magento e-commerce platform, implementing industry best practices and advanced testing patterns. Built with Python and Selenium WebDriver, this framework demonstrates a robust approach to automated testing using the Page Object Model (POM) design pattern.

### 🌟 Key Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Parallel Execution**: Optimized test execution with pytest-xdist
- **Rich Reporting**: Detailed test reports with Allure
- **CI/CD Integration**: Automated testing pipeline with GitHub Actions
- **GitHub Actions integration**: Published test reports to GitHub Pages
- **Type Safety**: Comprehensive type hints for better code quality
- **Logging**: Structured logging with custom formatters

## 🛠️ Technical Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.9+ |
| Testing Framework | pytest |
| Automation Tool | Selenium WebDriver |
| Reporting | Allure |
| CI/CD | GitHub Actions |
| Version Control | Git |
| Code Style | Black, isort |
| Browser Driver | ChromeDriver |

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Chrome browser
- ChromeDriver (matching your Chrome version)
- Git
- Allure (for reporting)

## 🚀 Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/summerduck/magento-selenium-test-framework-pom-python.git
cd magento-selenium-test-framework-pom-python
```

2. **Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Unix/macOS
.\venv\Scripts\activate   # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Tests**
```bash
# Run all tests
pytest

# Run tests in parallel
pytest -n auto

# Generate Allure report
allure serve allure-report
```

## 📊 Test Categories

| Category | Description | Command |
|----------|-------------|---------|
| Smoke | Critical path tests | `pytest -m smoke` |
| UI/UX | Interface tests | `pytest -m ui_ux` |

## 📁 Project Structure

```plaintext
magento-selenium-test-framework-pom-python/
├── pages/                # Page Object Models
│   ├── base_page.py      # Base page class
│   └── ...               # Individual page classes
├── tests/                # Test suites
│   ├── conftest.py       # pytest fixtures
│   └── ...               # Test modules
├── data/                 # Test data
├── utils/                # Utilities and helpers
├── conftest.py           # Global pytest fixtures and configuration
├── pytest.ini            # pytest configuration file
├── .env                  # Environment variables
└── requirements.txt      # Project dependencies
```

## 🎯 Highlights

- **Modern Architecture**: Current testing best practices
- **Clean Code**: Maintainable, well-documented code
- **Enterprise Patterns**: Industry-standard design patterns
- **Quality Focus**: Comprehensive testing approach with multiple test types
- **CI/CD Integration**: DevOps knowledge and automation skills

## 🎭 Enhancements

- Dramatic switch to playwright [Enterprise Playwright Test Automation Framework](https://github.com/summerduck/magento-playwright-test-framework-pom-python)

## 📝 Author

Darya Samardak - [LinkedIn](https://www.linkedin.com/in/darya-samardak/) - [GitHub](https://github.com/summerduck)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


