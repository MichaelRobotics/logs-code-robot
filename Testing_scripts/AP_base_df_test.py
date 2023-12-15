import pandas as pd

dat = {
'Robot': [9],
'TIME_START(started)': ["Initial"],
'TIME_END(Action completed)': ["Initial"],
'AP_NAME(started)': ["None"],
'ACTION_ERROR(waiting, aborted)': [0],
'DOCK_TRY(Position incorrect)': [0],
'DOCK_CORRECT(Position correct)': [0],
'UNDOCK_INCORRECT(Departure failed)': [0]
}

df2 = pd.DataFrame(dat)
print(df2)
