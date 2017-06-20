# lamport_mutex_hw

Заупск ручного режима:
```bash
python3 main.py --manual_mode True --pid 1
```

Запуск в режиме стресс теста:
```bash
python3 main.py --count 10
```

Запуск тестов:
```bash
python3 -m unittest tests/test_mock.py
```

Запуск анализатора:
```bash
python3 logs/loganylazer.py
```
