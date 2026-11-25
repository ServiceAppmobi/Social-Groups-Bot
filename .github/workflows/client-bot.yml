name: ServiceApp Client Bot

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - name: Pobierz kod
        uses: actions/checkout@v4
      - name: Ustaw Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Uruchom bota do klientow
        run: python client_bot.py
      - name: Zapisz wyniki
        uses: actions/upload-artifact@v4
        with:
          name: drafts-klient
          path: out/
