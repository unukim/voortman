import psycopg2

class database():
	def __init__(self, host, port, database, user, password):
		#connect to postgreSQL server 
		self.conn = psycopg2.connect(
			host = host, 
			port = port, 
			database = database, 
			user = user, 
			password = password, 
			)
		#define cursor to send SQL commend
		self.cur = self.conn.cursor()
		
	def insert_machine(self, model_type, bearing_type):
		#Check if the machine is registered before to the DB
		self.cur.execute(
			"SELECT id FROM machine WHERE model_type =%s AND bearing_type = %s",
			(model_type, bearing_type)
		)
		machine_id = self.cur.fetchone()
		if machine_id:
			return machine_id[0]
			
		#create new ID if a new model is registerd 
		query = """
		INSERT INTO machine (model_type, bearing_type)
		VALUES (%s, %s)
		RETURNING id;
		"""
		#send SQL commend to database. 
		self.cur.execute(query, (model_type, bearing_type))
		#read machine ID 
		new_machine_id = self.cur.fetchone()[0]
		self.conn.commit()
		return new_machine_id
			

	def insert_session(self, machine_id, start_time, duration):
		query = """
		INSERT INTO session(machine_id, start_time, duration)
		VALUES(%s, %s, %s)
		RETURNING id;
		"""
		
		self.cur.execute(query, (machine_id, start_time, duration))
		session_id = self.cur.fetchone()[0]
		self.conn.commit()
		return session_id
		
	def insert_raw_data(self, session_id, timestamp, sample):
		query = """
		INSERT INTO raw_data(session_id, timestamp, x, y, z)
		VALUES (%s, %s, %s, %s, %s)
		"""
		
		self.cur.execute(query, (
			session_id, 
			timestamp, 
			sample["x"], 
			sample["y"],
			sample["z"]
			))
		
		self.conn.commit()
	
	def connection_close(self):
		self.cur.close()
		self.conn.close()
		
	
		
