# Find OTA Revenue

Set the right price on OTAs. Enter how much you want to receive, add the OTA's commission and promo percentages, and get the price to list.

## Usage

```
find_ota_revenue.exe
```

1. Enter the **amount you want to receive** in *Input (result)*.
2. Add the OTA's percentage deductions in **Bracket 1** and **Bracket 2** (promos, commission, fees).
3. Click **Calculate x**.

## Build

```
pip install nuitka
python -m nuitka --standalone --onefile --windows-console-mode=disable --enable-plugin=tk-inter --output-dir=. find_ota_revenue.py
```


