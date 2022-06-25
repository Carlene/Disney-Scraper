####################### Standard Libraries #####################################
import pandas as pd
from datetime import datetime as dt, timedelta
####################### My Libraries ###########################################
from run import main
######################## Use Case ##############################################

yesterday = dt.today().date() - timedelta(days=1)
date = "2022-06-11"
date = dt.strptime(date, '%Y-%m-%d').date()
diff = abs(yesterday - date).days
print(diff)

for day in range(diff): # grab every date up to two days ago
    backfill_date = str(date + timedelta(days=day))
    main(start_date=backfill_date)

# dates_to_backfill = [for date in ]
# for date in 