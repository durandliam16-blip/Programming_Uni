#Ex8
def syracuse(nb):
    liste = [nb]
    while nb != 1:
        if nb % 2 == 0:
            nb = nb // 2
        else:
            nb = 3 * nb + 1
        liste.append(nb)
    return liste
max=0
for i in range(1,1000):
    if len(syracuse(i))>max:
        max=len(syracuse(i))
        nombre=i
print(nombre,max)

#Ex9
def bissextile(year):
    if (year % 4 == 0):
        if year % 100 != 0:
            return True
        else: 
            if year % 400 == 0:
                return True
            else:
                return False
    else:
        return False

def count_sundays(start_year, end_year):
    # Days in each month (for non-leap years):
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # 0: Monday, ..., 6: Sunday:
    day_of_week = 0  # 1 Jan 1900 is Monday
    count = 0
    for year in range(start_year, end_year + 1):
        for month in range(12):
            if day_of_week == 6:
                count += 1
            # Advance day_of_week by days in current month
            days = month_days[month]
            if month == 1 and bissextile(year):
                days += 1
            day_of_week = (day_of_week + days) % 7
    return count

#Compter les dimanches premiers du mois de 1901 à 2000 
#print(count_sundays(1901, 2000))
