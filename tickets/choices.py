class TicketsType:
    REGULAR = "regular"
    PREMIUM = "premium"
    VIP = "vip"

    CHOICES = (
        (REGULAR, "Regular ticket"),
        (PREMIUM, "Premium ticket"),
        (VIP, "Vip ticket"),
    )

    CHOICES_VALUES = [x[0] for x in CHOICES]
