import requests
import random
import logging

from pybelugaxl._models import BelugaPhoto
from .exceptions import InvalidRegistrationError

logger = logging.getLogger(__name__)

def get_images(registration: str = None, limit:int=3) -> list[BelugaPhoto]:
    #Credits for the JETAPI project, which is used to get the images of the Beluga planes.
    #Author: Macsen Casaus
    #Link: https://github.com/macsencasaus/jetapi

    """
    Get images of a Beluga aircraft from JetPhotos using unofficial JetPhotos API (https://github.com/macsencasaus/jetapi).

    Args:
        registration (str, optional): The registration number of the Beluga to filter by. ("F-GXLG" for example).
                                      If not provided, a random Beluga registration is selected.
        limit (int, optional): The maximum number of images to retrieve (default is 3, max is 15).

    Returns:
        list[BelugaPhoto]: A list of BelugaPhoto objects containing image metadata.
    """
    allowed_registrations = ["F-GXLG", "F-GXLH", "F-GXLI", "F-GXLJ", "F-GXLN", "F-GXLO"] #harcoded list ?

    if registration:
        registration = registration.upper()
        if len(registration) < 5 or len(registration) > 7:
            raise InvalidRegistrationError("Invalid registration. Please provide a valid plane registration number.")
        
        if registration not in allowed_registrations:
            raise InvalidRegistrationError(f"Woops.. That is not a BelugaXL registration. Must be one of: {', '.join(allowed_registrations)}")
    else:
        registration = random.choice(allowed_registrations) #randomly select a beluga if no registration is given

    if limit != 3:
        if not isinstance(limit, int) or limit < 1 or limit > 15:
            raise ValueError("Invalid limit. Please provide an integer between 1 and 15.")

    try:
        response = requests.get(f"https://www.jetapi.dev/api?reg={registration}&photos={limit}&only_jp=true", timeout=10)
        results = []

        if response.status_code == 200:
            data = response.json()
            
            if "Images" not in data or len(data["Images"]) == 0:
                logger.warning(f"No images found for registration {registration}")
                return []
            
            images = data["Images"]
            random.shuffle(images) #shuffle images to get a random selection every time
            
            for img in images:
                results.append(
                    BelugaPhoto(
                        registration=registration,
                        url=img["Image"] if "Image" in img else None,
                        photographer=img["Photographer"] if "Photographer" in img else "Unknown",
                        location=img["Location"] if "Location" in img else "Unknown",
                        date_taken=img["DateTaken"] if "DateTaken" in img else "Unknown",
                        date_uploaded=img["DateUploaded"] if "DateUploaded" in img else "Unknown"
                    )
                )

            return results
        else:
            logger.error(f"Failed to fetch images for registration {registration}. Status code: {response.status_code}")
            return []
        
    except Exception as e:
        logger.error(f"Error fetching images for registration {registration}: {e}")
        return []


if __name__ == "__main__":
    print(get_images("F-GXLG", limit=5))