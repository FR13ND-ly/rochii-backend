def getImage(image):
    res = {
        "id": 0,
        "name": "",
    }
    if image:
        res = {
            "id": image.id,
            "name": image.name,
        }
    
    return res