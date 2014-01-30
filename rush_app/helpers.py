from django.templatetags.static import static

def get_schools():
    return []
#     school_choices = []
#     with open(static("txt/colleges.txt"), 'rb') as f:
#         for school in f:
#             school_choices.append((school, school))
#     return school_choices