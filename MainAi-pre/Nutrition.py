from fpdf import FPDF

# Input should be weight, height and age

def bmr_calc(weight, height, age):
    BMR = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age
    return BMR

# Input should be goal which is 1 for keeping the wieght, 2 for cutting, 3 for bulking and activity level which is from 0 to 4, the bmr
def cals(goal, level, bmr):
    levels_factors = [1.2,1.375,1.55,1.725,1.9]
    factor = levels_factors[level]
    goals = [0,-500,500]
    return bmr * factor + goals[goal]

# Input should be the calories and goal ( 0 - normal, 1 - new body builder), and body weight
def macros(cals,goal, weight):
    if goal == 0:
        proteins = round(weight * 0.8)
        fats = round(cals * 0.3 / 9)
        carbs = round((cals - (proteins * 4 + fats * 9)) / 4)
        return ["proteins: " + str(proteins), "carbs: " + str(carbs), "fats: " + str(fats)]
    else:
        proteins = round(weight * 2)
        fats = round(cals * 0.3 / 9)
        carbs = round((cals - (proteins * 4 + fats * 9)) / 4)
        return ["proteins: " + str(proteins), "carbs: " + str(carbs), "fats: " + str(fats)]


pdf = FPDF()

# Add a page
pdf.add_page()

# Set font
pdf.set_font("Arial", size = 12)

# Add list items to PDF
for item in macros(2000, 1, 66):
    pdf.cell(200, 10, txt = item, ln = True, align = 'L')

# Output the PDF
pdf.output("my_list.pdf")