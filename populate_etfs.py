import config
import alpaca_trade_api as tradeapi
import psycopg2 
import psycopg2.extras
import csv

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
# cursor.execute(
#     """
#     Select * 
#     from stock
#     where is_etf = TRUE;
#     """
# )

# rows = cursor.fetchall()
# print(rows)

cursor.execute("select * from stock where is_etf = TRUE")
etfs = cursor.fetchall()

dates = ['2021-02-03']
for current_date in dates:
    for etf in etfs:
        try: 
            print(etf['symbol'])
            with open (f"data/{current_date}/{etf['symbol']}.csv") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    ticker = row[3]
                    
                    if ticker:
                        shares = row[5]
                        weight = row[7]

                        # cursor.execute([], values) takes a tuple as values
                        # in Python, a tuple containing a single value must include a comma. 
                        # For example, ('abc') is evaluated as a scalar while ('abc',) 
                        # is evaluated as a tuple. 
                        cursor.execute("""
                            SELECT * FROM stock WHERE symbol = %s
                        """, (ticker,))

                        stock = cursor.fetchone()
                        if stock:
                            cursor.execute("""
                                INSERT INTO etf_holding (etf_id, holding_id, dt, shares, weight)
                                VALUES (%s, %s, %s, %s, %s)
                            """,(etf['id'], stock['id'], current_date, shares, weight))
                        else:
                            print("NULL stock")
        except:
            print(f"*{etf['symbol']} stock is not part of the data or date of\nfile not present or sql operation incorrect.*")
connection.commit()