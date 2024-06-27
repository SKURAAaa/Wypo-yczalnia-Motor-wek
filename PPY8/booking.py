class Booking:
    def __init__(self, user, boat, dateFrom, days):
        self.boat = boat  # Motorówka zarezerwowana
        self.user = user  # Użytkownik dokonujący rezerwacji
        self.dateFrom = dateFrom  # Data rozpoczęcia rezerwacji
        self.days = days  # Liczba dni rezerwacji
        self.cost = self.boat.costPerDay * days  # Całkowity koszt rezerwacji
