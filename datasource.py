import psycopg2
import getpass

class Nutrek:
    '''
    Nutrek executes all of the queries on the database
    and formats the data to send back to the front end'''


    def connect(self, user, password):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman
            Note: exits if a connection cannot be established.
        '''
        try:
            self.connection = psycopg2.connect(host="localhost", database=user, user=user, password=password)
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def disconnect(self):
        '''
        Breaks the connection to the database
        '''
        self.connection.close()

    def getNutrients(self, food):
        '''
        returns all nutrients and the amount of each nutrient in a given food
        '''
        food = food.upper()
        nutrientList = ["Ash(g)", "Biotin(mcg)", "Caffeine(mg)", "Calcium(mg)", "Carbohydrate by difference(g)", "Carbohydrate_other(g)", "Cholesterol(mg)",
        "Chromium(mcg)", "Copper(mg)", "Fatty acids total monounsaturated(g)", "Fatty acids total polyunsaturated (g)", "Fatty acids total saturated(g)", "Fatty acids total trans(g)",
        "Fiber insoluble(g)", "Fiber soluble(g)", "Fiber total dietary(g)", "Folic acid(mcg)", "Iodine(mcg)", "Iron(mg)", "Lactose(g)",
         "Magnesium(mg)", "Manganese(mg)", "Niacin(mg)", "Pantothenic acid(mg)", "Phosphorus (mg)", "Potassium(mg)",
         "Protein(g)", "Riboflavin(mg)", "Selenium(mcg)", "Sodium(mg)", "Sugars added(g)", "Sugars total(g)", "Thiamin(mg)", "Total lipid fat(g)",
         "Total sugar alcohols(g)", "Vitamin A IU" , "Vitamin B-12(mcg)", "Vitamin-B6(mg)", "Vitamin C total ascorbic acid(mg)",
         "Vitamin D IU", "Vitamin E label entry primarily IU", "Vitamin K phylloquinone(mcg)", "Water(g)",
         "Xylitol(g)", "Zinc(mg)"]
        try:
            cursor1 = self.connection.cursor()
            cursor1.execute("SELECT Ash_grams, Biotin_mcg, Caffeine_mg, Calcium_Ca_mg, Carbohydrate_by_difference_g, Carbohydrate_other_g, Cholesterol_mg, Chromium_Cr_mcg, Copper_Cu_mg, Fatty_acids_total_monounsaturated_g, Fatty_acids_total_polyunsaturated_g, Fatty_acids_total_saturated_g, Fatty_acids_total_trans_g, Fiber_insoluble_g, Fiber_soluble_g, Fiber_total_dietary_g, Folic_acid_mcg, Iodine_I_mcg, Iron_Fe_mg, Lactose_g, Magnesium_Mg_mg, Manganese_Mn_mg, Niacin_mg, Pantothenic_acid_mg FROM Nutrek WHERE food_name LIKE " + str("'%"+food+"%'") + ";")
            results1 = cursor1.fetchall()
            cursor2 = self.connection.cursor()
            cursor2.execute("SELECT Phosphorus_P_mg, Potassium_K_mg, Protein_g, Riboflavin_mg, Selenium_Se_mcg, Sodium_Na_mg, Sugars_added_g, Sugars_total_g, Thiamin_mg, Total_lipid_fat_g, Total_sugar_alcohols_g, Vitamin_A_IU , Vitamin_B12_mcg, Vitamin_B6_mg, Vitamin_C_total_ascorbic_acid_mg, Vitamin_D_IU, Vitamin_E_label_entry_primarily_IU, Vitamin_K_phylloquinone_mcg, Water_g, Xylitol_g, Zinc_Zn_mg FROM Nutrek WHERE food_name LIKE " + str("'%"+food+"%'") + ";")
            results2 = cursor2.fetchall()
            fullNutrientList = []
            results = results1 + results2
            nutrientDictionary = {}
            finalResult = results[0]
            for nutrient, proportion in zip(nutrientList, finalResult):
                nutrientDictionary[nutrient] = proportion
            return nutrientDictionary

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getIngredientBreakDown(self, food):
        ''' returns all the ingredients in a given food item'''
        food = food.upper()
        try:
            cursor = self.connection.cursor()
            query = ("SELECT ingredients_english FROM Nutrek WHERE  food_name LIKE " + str("'%"+food+"%'") +";")
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getFoodAvailable(self):
        '''returns all foods in database'''
        try:
            cursor = connection.cursor()
            query = "SELECT food_name FROM Nutrek"
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def containsAllergen(self, food, allergen):
        '''returns True if food contains allergen (could cause allergic reaction) and false if otherwise '''

        ingredients = self.getIngredientBreakDown(food)
        finalIngredients = ingredients.split(" ")
        FullIngredientList = []
        allergen = allergen.upper()
        for item in finalIngredients:
            if "(" in item:
                item = item.replace("(", "")
            if "," in item:
                item = item.replace(",", "")
            if ")" in item:
                item = item.replace(")","")
            FullIngredientList.append(item)
        food = food.upper()
        try:
            for ing in FullIngredientList:
                if allergen in ing:
                    return True
            return False
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None



    def getNutrientThreshold(self, food, nutrient, nutritionTarget):
        '''check if the amount of nutrients in a given food is meeting the indicated goal for a user
        we need to define this. Greater or Less than?'''
        food = food.upper()
        nutrient = nutrient.lower()
        nutrientDictionary = self.getNutrients(food)

        try:
            for item in nutrientDictionary:
                item = item.lower()
                if nutrient in item:
                    return nutrient, nutrientDictionary[item]

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

        pass

def main():
    user = 'odoome'
    password = 'tiger672carpet'
    #password = getpass.getpass()

    # Connect to the database
    N = Nutrek()
    N.connect(user, password)
    print(N.getNutrients('granola'))
    #print(N.getIngredientBreakDown('granola'))
    #print(N.containsAllergen('granola', 'peanut'))
    print(N.getNutrientThreshold('granola', 'protein', 0.5))

    # Disconnect from database
    N.disconnect()
main()
