import dtuple

fieldlist=["name", "Num", "LinkText"]
descr=dtuple.TupleDescriptor([[n] for n in fieldlist])
#descr=dtuple.TupleDescriptor(curs.description)
#......
row=dtuple.DatabaseTuple(descr,row)
#row[0] .. row["Name"]
#......
