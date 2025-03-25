text = resume.pdf
keywords = ["any", "these", "missing"]

if any(keyword in text for keyword in keywords):
    print("At least one keyword found.")
else:
    print("No keyword found.")