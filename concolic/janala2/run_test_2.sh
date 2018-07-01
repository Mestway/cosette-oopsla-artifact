>&2 echo "start"
>&2 echo "equiv1a"

time python concolic.py --coverage 20 custom.EquivTest1a 10 > equiv1a_20_10.log
time python concolic.py --coverage 20 custom.EquivTest1a 20 > equiv1a_20_20.log
time python concolic.py --coverage 20 custom.EquivTest1a 30 > equiv1a_20_30.log
time python concolic.py --coverage 20 custom.EquivTest1a 40 > equiv1a_20_40.log
time python concolic.py --coverage 20 custom.EquivTest1a 50 > equiv1a_20_50.log
time python concolic.py --coverage 20 custom.EquivTest1a 60 > equiv1a_20_60.log
time python concolic.py --coverage 20 custom.EquivTest1a 70 > equiv1a_20_70.log
time python concolic.py --coverage 20 custom.EquivTest1a 80 > equiv1a_20_80.log
time python concolic.py --coverage 20 custom.EquivTest1a 90 > equiv1a_20_90.log
time python concolic.py --coverage 20 custom.EquivTest1a 100 > equiv1a_20_100.log

>&2 echo "equiv1b"

time python concolic.py --coverage 20 custom.EquivTest1b 10 > equiv1b_20_10.log
time python concolic.py --coverage 20 custom.EquivTest1b 20 > equiv1b_20_20.log
time python concolic.py --coverage 20 custom.EquivTest1b 30 > equiv1b_20_30.log
time python concolic.py --coverage 20 custom.EquivTest1b 40 > equiv1b_20_40.log
time python concolic.py --coverage 20 custom.EquivTest1b 50 > equiv1b_20_50.log
time python concolic.py --coverage 20 custom.EquivTest1b 60 > equiv1b_20_60.log
time python concolic.py --coverage 20 custom.EquivTest1b 70 > equiv1b_20_70.log
time python concolic.py --coverage 20 custom.EquivTest1b 80 > equiv1b_20_80.log
time python concolic.py --coverage 20 custom.EquivTest1b 90 > equiv1b_20_90.log
time python concolic.py --coverage 20 custom.EquivTest1b 100 > equiv1b_20_100.log
