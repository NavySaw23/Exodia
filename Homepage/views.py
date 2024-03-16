from django.shortcuts import render


def create_list():
  class Spots:
    def __init__(self):
      # name location scale scaleUni shelterlist
      self.disaster1 = "disaster1"
      self.location1 = "city1"
      self.scale1 = "5"
      self.UniScale1 = "3"
      self.shelterlist1 = ["1","2","etc"]
  spots = Spots()
  return spots


# Create your views here.
def home_view(request, *args, **kwargs):
    # whatever function is fetching City and Country name of current location, should return here
    city = "Dehradun"
    country = "India"

    hotspots = create_list()

    context = {
        'location' : city,
        'country' : country,
        'list' : hotspots,
    }
    return render(request, 'home.html', context)

