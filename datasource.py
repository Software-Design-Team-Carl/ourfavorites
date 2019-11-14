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
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT food_name FROM Nutrek WHERE food_name LIKE " + str("'%"+food+"%'") +";")
            results = cursor.fetchall()
            return results

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
        while "(" in finalIngredients:
            finalIngredients.remove("(")
        food = food.upper()
        try:
            return finalIngredients
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None



    def getNutrientThreshold(self, food, nutrient, nutritionTarget):
        '''check if the amount of nutrients in a given food is meeting the indicated goal for a user'''
        food = food.upper()
        try:
            cursor = connection.cursor()
            query = ("")
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

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
    #print(N.getNutrients('granola'))
    print(N.getIngredientBreakDown('granola'))
    print(N.containsAllergen('granola', 'peanuts'))

    # Disconnect from database
    N.disconnect()
main()
