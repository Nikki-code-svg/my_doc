from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt 
from datetime import datetime

# Association table
doctor_note_patient = db.Table('doctor_note_patient',
    db.Column('doctor_note_id', db.Integer, db.ForeignKey('doctors_notes.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patients_table.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):

  __tablename__ = 'users_table'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable=False)
  password_hash= db.Column(db.String, nullable=False)

  doctor = db.relationship('Doctor', uselist=False, back_populates='user')
 
  serialize_rules = ("-password_hash",)

  @property
  def password(self): 
      raise Exception("Safety First")
    
  @password.setter
  def password(self, value): 
      self.password_hash = bcrypt.generate_password_hash(value).decode('utf-8')

  def authenticate(self, password_to_check): 
      return bcrypt.check_password_hash(self.password_hash, password_to_check) 

class Doctor(db.Model, SerializerMixin):
  
  __tablename__ = 'doctors_table'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  specialty = db.Column(db.String)
  # doctor_note_id = db.Column(db.String, db.ForeignKey('doctors_notes.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users_table.id'))

  user = db.relationship('User', back_populates='doctor')
  notes = db.relationship('DoctorNote', back_populates='doctor', cascade='all, delete-orphan')
  appointments = db.relationship('Appointment', back_populates='doctor')

  serialize_rules = ('-appointments.doctor', '-notes.doctor',)



class Appointment(db.Model, SerializerMixin):
  __tablename__ = 'appointments_table'
  

  id = db.Column(db.Integer, primary_key=True)
  datetime = db.Column(db.DateTime)
  doctor_id = db.Column(db.Integer, db.ForeignKey('doctors_table.id'), nullable=False)
  patient_id = db.Column(db.Integer, db.ForeignKey('patients_table.id'), nullable=False)

  patient = db.relationship('Patient', back_populates='appointments')
  doctor = db.relationship('Doctor', back_populates='appointments')

  serialize_rules = ('-patient.appointments', '-doctor.appointments',)



class Patient(db.Model, SerializerMixin):

  __tablename__ = 'patients_table'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  dob = db.Column(db.Integer, nullable=False)
  chart_id = db.Column(db.String, db.ForeignKey('chart_table.id'), nullable=False)

  appointments = db.relationship('Appointment', back_populates='patient')
  doctor_notes = db.relationship('DoctorNote', secondary='doctor_note_patient', back_populates='patients')

  serialize_rules = ('appointments.patient', 'doctor_notes.patients',)


class DoctorNote(db.Model, SerializerMixin):
  __tablename__ = 'doctors_notes'

  id = db.Column(db.Integer, primary_key=True)
  note = db.Column(db.String)
  date = db.Column(db.DateTime)
  doctor_id = db.Column(db.Integer, db.ForeignKey('doctors_table.id'))

  doctor = db.relationship('Doctor', back_populates='notes')
# not every user can access and post doctor notes, only doctor-users can do so 
  patients = db.relationship('Patient', secondary='doctor_note_patient', back_populates='doctor_notes')

class Chart(db.Model, SerializerMixin):
  __tablename__ = 'chart_table'

  id = db.Column(db.Integer, primary_key=True)
  info = db.Column(db.String)


