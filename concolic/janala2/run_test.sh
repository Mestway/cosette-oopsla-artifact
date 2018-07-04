touch time.txt
rm time.txt

>&2 echo "start"
>&2 echo "equiv1a"

{ time python concolic.py --coverage 20 custom.EquivTest1a 10 > equiv1a_20_10.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 20 > equiv1a_20_20.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 30 > equiv1a_20_30.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 40 > equiv1a_20_40.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 50 > equiv1a_20_50.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 60 > equiv1a_20_60.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 70 > equiv1a_20_70.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 80 > equiv1a_20_80.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 90 > equiv1a_20_90.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1a 100 > equiv1a_20_100.log ; } 2>> time.txt

>&2 echo "equiv1b"

{ time python concolic.py --coverage 20 custom.EquivTest1b 10 > equiv1b_20_10.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 20 > equiv1b_20_20.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 30 > equiv1b_20_30.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 40 > equiv1b_20_40.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 50 > equiv1b_20_50.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 60 > equiv1b_20_60.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 70 > equiv1b_20_70.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 80 > equiv1b_20_80.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 90 > equiv1b_20_90.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest1b 100 > equiv1b_20_100.log ; } 2>> time.txt

>&2 echo "equiv2a"

{ time python concolic.py --coverage 20 custom.EquivTest2a 10 > equiv2a_20_10.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 20 > equiv2a_20_20.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 30 > equiv2a_20_30.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 40 > equiv2a_20_40.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 50 > equiv2a_20_50.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 60 > equiv2a_20_60.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 70 > equiv2a_20_70.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 80 > equiv2a_20_80.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 90 > equiv2a_20_90.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2a 100 > equiv2a_20_100.log ; } 2>> time.txt

>&2 echo "equiv2b"

{ time python concolic.py --coverage 20 custom.EquivTest2b 10 > equiv2b_20_10.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 20 > equiv2b_20_20.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 30 > equiv2b_20_30.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 40 > equiv2b_20_40.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 50 > equiv2b_20_50.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 60 > equiv2b_20_60.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 70 > equiv2b_20_70.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 80 > equiv2b_20_80.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 90 > equiv2b_20_90.log ; } 2>> time.txt
{ time python concolic.py --coverage 20 custom.EquivTest2b 100 > equiv2b_20_100.log ; } 2>> time.txt
