# Sample ad copy bank
# Structure: SAMPLES[product][keyword] = {variants: [...], product_desc: str, url: str}

SAMPLES = {
    "Nike Running Shoes": {
        "buy nike running shoes online": {
            "product_desc": "Nike Running Shoes — engineered for performance. Available in React foam and Air Zoom cushioning variants for training, racing, and everyday running. Free delivery on orders over ₹3,000. 30-day returns.",
            "url": "nike.com",
            "intent": "Purchase",
            "variants": [
                {
                    "label": "Variant A — Ready to serve",
                    "headline": "Nike Running Shoes – Shop Now",
                    "description": "Free delivery over ₹3,000. React foam for speed. New arrivals in stock. Order today.",
                },
                {
                    "label": "Variant B — Needs revision",
                    "headline": "Nike Shoes – Great for Running",
                    "description": "Nike offers a wide range of running shoes with comfort and style for all types of runners.",
                },
                {
                    "label": "Variant C — Reject",
                    "headline": "Explore Nike Footwear Online",
                    "description": "Nike has been making shoes for years. Learn about our products and find out more online.",
                },
            ],
        },
        "best running shoes for marathon training": {
            "product_desc": "Nike Running Shoes — engineered for performance. Available in React foam and Air Zoom cushioning variants for training, racing, and everyday running. Free delivery on orders over ₹3,000. 30-day returns.",
            "url": "nike.com",
            "intent": "Consideration",
            "variants": [
                {
                    "label": "Variant A — Ready to serve",
                    "headline": "Marathon-Ready Nike – Compare",
                    "description": "React vs Air Zoom: Nike's top marathon trainers compared. Find your match before race day.",
                },
                {
                    "label": "Variant B — Needs revision",
                    "headline": "Nike Marathon Shoes – Buy Now",
                    "description": "Top-rated Nike running shoes for marathon training. Advanced cushioning for long runs.",
                },
                {
                    "label": "Variant C — Reject",
                    "headline": "Nike Running Shoes Available",
                    "description": "Shop Nike running shoes online. We have many options for runners. Visit our website today.",
                },
            ],
        },
    },
    "Trello": {
        "project management tool for teams": {
            "product_desc": "Trello is a visual project management tool that uses boards, lists, and cards to help teams organise work. Available on Free, Standard, and Premium plans. 2M+ teams worldwide. 100+ integrations including Slack, Google Drive, and Jira.",
            "url": "trello.com",
            "intent": "Consideration",
            "variants": [
                {
                    "label": "Variant A — Ready to serve",
                    "headline": "Trello for Teams – See How",
                    "description": "Visual boards, 100+ integrations. See why 2M+ teams choose Trello. Free to start.",
                },
                {
                    "label": "Variant B — Needs revision",
                    "headline": "Trello – Manage Team Projects",
                    "description": "Trello helps teams manage projects using boards, lists, and cards to organise work better.",
                },
                {
                    "label": "Variant C — Reject",
                    "headline": "Project Management Software",
                    "description": "Looking for a way to manage projects? Trello is a tool that can help your team.",
                },
            ],
        },
        "buy trello premium plan": {
            "product_desc": "Trello is a visual project management tool that uses boards, lists, and cards to help teams organise work. Available on Free, Standard, and Premium plans. 2M+ teams worldwide. 100+ integrations including Slack, Google Drive, and Jira.",
            "url": "trello.com",
            "intent": "Purchase",
            "variants": [
                {
                    "label": "Variant A — Ready to serve",
                    "headline": "Trello Premium – Start Today",
                    "description": "Unlimited boards, priority support, advanced checklists. ₹840/user/month. Upgrade now.",
                },
                {
                    "label": "Variant B — Needs revision",
                    "headline": "Upgrade to Trello Premium",
                    "description": "Trello Premium unlocks more features and better tools for your team's project management.",
                },
                {
                    "label": "Variant C — Reject",
                    "headline": "What Is Trello Premium?",
                    "description": "Trello Premium is our paid plan offering additional features for teams wanting more.",
                },
            ],
        },
    },
    "MakeMyTrip": {
        "cheap flights to Goa this weekend": {
            "product_desc": "MakeMyTrip is India's leading travel booking platform for flights, hotels, and holiday packages. Lowest fare guarantee, instant booking confirmation, and 24/7 customer support. 500+ routes across India. Price calendar and fare alert features available.",
            "url": "makemytrip.com",
            "intent": "Purchase",
            "variants": [
                {
                    "label": "Variant A — Ready to serve",
                    "headline": "Goa Flights ₹1,899 – Book Now",
                    "description": "Last-minute seats filling fast. Lowest fare guarantee + instant confirmation. Book now.",
                },
                {
                    "label": "Variant B — Needs revision",
                    "headline": "Fly to Goa This Weekend",
                    "description": "Find great deals on weekend flights to Goa on MakeMyTrip. Compare options and book easily.",
                },
                {
                    "label": "Variant C — Reject",
                    "headline": "MakeMyTrip Flight Booking",
                    "description": "MakeMyTrip offers flight booking across India. Explore our options and learn more.",
                },
            ],
        },
        "compare flight prices india": {
            "product_desc": "MakeMyTrip is India's leading travel booking platform for flights, hotels, and holiday packages. Lowest fare guarantee, instant booking confirmation, and 24/7 customer support. 500+ routes across India. Price calendar and fare alert features available.",
            "url": "makemytrip.com",
            "intent": "Consideration",
            "variants": [
                {
                    "label": "Variant A — Ready to serve",
                    "headline": "Compare India Flights – Free",
                    "description": "Price calendar, fare alerts, 500+ routes. Compare and lock the best fare on MakeMyTrip.",
                },
                {
                    "label": "Variant B — Needs revision",
                    "headline": "Best Flight Prices – Book Now",
                    "description": "MakeMyTrip shows lowest flight prices across all major airlines in India. Book today.",
                },
                {
                    "label": "Variant C — Reject",
                    "headline": "Flights Available on MMT",
                    "description": "Compare flight prices on MakeMyTrip. We have many airlines and routes to choose from.",
                },
            ],
        },
    },
}

# Flat list of all samples for random selection in Evaluate tab
ALL_SAMPLES = []
for product, keywords in SAMPLES.items():
    for keyword, data in keywords.items():
        for variant in data["variants"]:
            ALL_SAMPLES.append({
                "product": product,
                "keyword": keyword,
                "product_desc": data["product_desc"],
                "url": data["url"],
                "intent": data["intent"],
                "headline": variant["headline"],
                "description": variant["description"],
                "label": variant["label"],
            })