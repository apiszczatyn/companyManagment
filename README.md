# Company Management

Company Management to aplikacja desktopowa napisana w Pythonie, służąca do podstawowego zarządzania danymi w firmie. Projekt umożliwia obsługę pracowników oraz zamówień, a także integrację z bazą danych lub systemem zapisu danych.

Aplikacja została zaprojektowana jako prosty system wspomagający zarządzanie małą lub średnią firmą.

---

## Funkcjonalności

- Zarządzanie pracownikami
  - dodawanie, edytowanie i usuwanie pracowników
  - przegląd listy pracowników

- Zarządzanie zamówieniami
  - dodawanie i obsługa zamówień
  - przegląd istniejących zamówień

- Główne okno aplikacji
  - centralny interfejs użytkownika
  - dostęp do wszystkich modułów systemu

- Komunikacja z bazą danych
  - zapisywanie i odczyt danych
  - oddzielna warstwa logiki bazodanowej

---

## Struktura projektu

Projekt składa się z następujących głównych plików:

- `companyManagment.py` – punkt startowy aplikacji  
- `mainWindow.py` – główne okno i logika interfejsu  
- `employeesManagment.py` – moduł zarządzania pracownikami  
- `ordersManagment.py` – moduł zarządzania zamówieniami  
- `dbCom.py` – obsługa komunikacji z bazą danych  
- `images/` – zasoby graficzne używane w aplikacji  

---

## Wymagania

- Python 3.x
- System operacyjny: Windows / Linux / macOS
