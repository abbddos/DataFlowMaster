from database import db 
import datetime 


class RefugeeRegistration(db.Model):
    __tablename__ = "refugees"
    
    id = db.Column(db.Integer, primary_key = True)
    camp = db.Column(db.String(50), nullable = False)
    firstName = db.Column(db.String(50), nullable = False)
    middleName = db.Column(db.String(50), nullable = True)
    lastName = db.Column(db.String(50), nullable = False)
    sex = db.Column(db.String(10), nullable = False)
    dateOfBirth = db.Column(db.DateTime, nullable = False)
    placeOfBirth = db.Column(db.String(150), nullable = False)
    nationality = db.Column(db.String(150), nullable = False)
    ethnicity = db.Column(db.String(50), nullable = True)
    religion = db.Column(db.String(50), nullable = True)
    householdSize = db.Column(db.Integer, nullable = False)
    householdHasDisability = db.Column(db.Boolean, default = False)
    disabilityType = db.Column(db.String(150), nullable = True)
    householdHasInfants = db.Column(db.Boolean, default = False)
    numOfInfants = db.Column(db.Integer, nullable = False, default = 0)
    householdHasElderly = db.Column(db.Boolean, default = False)
    numOfElderly = db.Column(db.Integer, nullable = False, default = 0)
    hasDocumentation = db.Column(db.Boolean, default = False)
    documentationType = db.Column(db.String(150), nullable = True)
    documentationNumber = db.Column(db.String(150), nullable = True)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    
    

    def __init__(self, camp, firstName, lastName, dateOfBirth, sex, placeOfBirth, nationality, householdSize, **kwargs):
        # Required fields
        self.camp = camp
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.sex = sex
        self.placeOfBirth = placeOfBirth
        self.nationality = nationality
        self.householdSize = householdSize
        
        
    def serialize(self):
        return {
            "id": self.id,
            "camp": self.camp,
            "firstName": self.firstName,
            "middleName": self.middleName,
            "lastName": self.lastName,
            "sex": self.sex,
            "dateOfBirth": self.dateOfBirth,
            "placeOfBirth": self.placeOfBirth,
            "nationality": self.nationality,
            "ethnicity": self.ethnicity,
            "religion": self.religion,
            "householdSize": self.householdSize,
            "householdHasDisability": self.householdHasDisability,
            "disabilityType": self.disabilityType,
            "householdHasInfants": self.householdHasInfants,
            "numOfInfants": self.numOfInfants,
            "householdHasElderly": self.householdHasElderly,
            "numOfElderly": self.numOfElderly,
            "hasDocumentation": self.hasDocumentation,
            "documentationType": self.documentationType,
            "documentationNumber": self.documentationNumber,
            "createdAt": self.createdAt
        }
