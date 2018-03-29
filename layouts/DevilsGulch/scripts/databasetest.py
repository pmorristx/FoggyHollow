from com.ziclix.python.sql import zxJDBC

connectionUrl = "jdbc:mysql://192.168.0.12:3306"
cnxn = zxJDBC.connect(
        connectionUrl,
        "foggyhollow",
        "foggyhollow",
        "com.mysql.jdbc.Driver")
crsr = cnxn.cursor()
crsr.execute("select * from foggyhollow.station_schedules where station='Beaver Bend'")
rows = crsr.fetchall()
print(rows)
