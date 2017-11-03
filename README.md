# Requires Python 2.7 and following dependencies:<br />
import sys <br />
import io <br />
from collections import defaultdict <br />
from numpy import median <br /> 
# Multiple test cases were made and tested against the manually verified results. Test cases include: <br />
1. OTHER_ID not empty <br />
2. Malformed and/or empty TRANSACTION_DT with good ZIP_CODE <br />
3. Fewer than 5 digits and/or empty ZIP_CODE with good TRANSACTION_DT <br />
4. CMTE_ID empty <br />
5. TRANSACTION_AMT empty 
