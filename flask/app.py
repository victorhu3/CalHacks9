from flask import Flask, jsonify, request
import json
import re
import requests
import pandas as pd
import numpy as np

import cohere
from cohere.classify import Example

prompt = '\nSummarize the suggestion:\nMy mother-in law was German add taught me how to make these 40 ye. ago. I make mine with onion and server them with ham and bean soup.\nSummary: Make with onion and serve with ham and bean soup\n--\nSummarize the suggestion:\nTwo eggs are not enough. I used three and it was still DRY (very tasty, but dry). Five or six would be much better - with two it was more like a pile of onions than an onion pie.\nSummary: Use five to six eggs instead of three\n--\nSummarize the suggestion:\nI love butter but added almonds. Next time I\'ll try toasted almonds. IH\nSummary: Add almonds or toasted almonds\n--\nSummarize the suggestion:\nThis salad is absolutely delicious. My husband didn\'t like it, however, because he doesn\'t like cilantro. You could substitute parsley or leave it out entirely, if you wanted, but I like it the way it is. I will make this often and am sharing it with my friends!\nSummary: Substitute parsley\n--\nSummarize the suggestion:\nI agree with the other comments (use fresh mozerella, etc.) It\'s hard to find in some areas. Trader Joe\'s has it. Italian deli\'s have it, if you are lucky enough to have one where you live. I just have one suggestion. Drizzle on some Balsamic vinegar along with the olive oil. I travelled all over Italy last summer and ate this salad everywhere. Many places added the Balsamic and it makes a good salad really good!\nSummary: Use fresh mozerella and drizzle on balsamic vinegar\n--\nSummarize the suggestion:\nThis was wonderful--finally got around to using the A to Z ingredients--and I used 2 cups of strawberries! this bread was great--it will be in my cookbook for good because of its totally unmatched level of versatility.\nSummary: Use strawberries\n--\nSummarize the suggestion:\nVery easy to make for a lunch. I served it cold as a sandwich. I found it a little too bland though. Next time I make it I will add some cheese (like blue cheese or sharp cheddar)\nSummary: Add some cheese\n--\nSummarize the suggestion:\nIt is actually a recipe for Shrimp Mousse, it should be poured into a greased mold, refrigerated\n \n then unmolded onto a serving plate. It really would not freeze well because of the ingredients.\nSummary: Pour this into a greased mold\n--\nSummarize the suggestion:\nJust like my Granny use to make but she.d swop raisins for currants occasionally.\nSummary: Swap raisins for currants\n--\nSummarize the suggestion:\nI did\'t have Mustard oil so used canola. Very tasty.\nSummary: Use canola instead of mustard oil\n--\nSummarize the suggestion:\nExcellent easy recipe - I made w/out coconut and it was still good. Also, substituted oat flour for the oat meal and it worked just fine.\nSummary: Make it without coconut.\n--\nSummarize the suggestion:\nThis was VERY good, and easy. My favorite combination. There were no leftovers at our house either. I added a little minced garlic and I cooked the chicken in a baking dish in half a can of chicken broth, I didn\'t add the other ingredients until the chicken had cooked a little, then added the cheese, and diluted the soup with the other half can of broth. I also instead of \"topping\" the chicken with the stuffing mix, put it between and all around the chicken. That way, you could see the chicken, and the stuffing.\nSummary: Add a little minced garlic and cook the chicken in a baking dish in half a can of chicken broth\n--\nSummarize the suggestion:\nI used small whole red potatoes instead of cutting up larger ones. Baked at 350 and added a little parsley for color. Absolutely delicious.\nSummary: Use small whole red potatoes and add parsley\n--\nSummarize the suggestion:\nI made this with breasts as well. I left the skin on (removing any excess fat) to avoid drying it out too much. It was great. I served it to my family and they all loved it. The left overs were even better the next day. Very easy, quick preparation and looks lovely served with saffron rice and fresh green beans. A great company dish.\nSummary: Make it with breasts and leave the skin on\n--\nSummarize the suggestion:\nI substituted nutritional yeast for the milk powder to veganize this, and black instead of green olives, and it turned out absolutely fantastic.\nSummary: Substitute nutritional yeast for milk and use black instead of green olives\n--\nSummarize the suggestion:\nTo me, basmati rice is the best. Instead of water I use chicken stock. It adds a little more flavor\nSummary: Use basmati rice and use chicken stock instead of water\n--\nSummarize the suggestion:\nI made this and froze it. I served it a week later and it was just fine. Lemon and blueberries go together in this recipe very well\nSummary: Freeze it\n--\nSummarize the suggestion:\nThis recipe needs to include some sliced carrots. I think they can be substituted for some of the peas, but they are definately something that needs to be added to break up the color a bit. About 1/2 cup should do.\nSummary: Include some sliced carrots instead of peas\n--\nSummarize the suggestion:\nThis was a very good meatloaf BUT to spicy for OUR TASTE. I omitted the oregano and garlic and added chopped bell pepper w/the onion. Added soft bread cubes to 2 tbs. milk, 1 tbs. Lea n Perrin, squished it all up well; added 1 well-beaten egg squishing more and squishing in about 3/4cup Ketchup. Patted into a 13x9 greased {Pam Spray} dish, w/hand made furrows across the top, laid raw sliced bacon strips on top. Baked at 325* to 350* about one (1) hour and drained grease/liquid from dish, removed bacon slices and poured{and spread evenly} about 1 cup Ketchup over top and continue cooking 30 minutes....my family love this version of this recipe.....especialy served with Dutchess Pototoes, dried Black-eyed peas, creamed corn, buttermilk cornbread and, if there is any room......Black-berry cobbler and vanilla ice cream.....THIS IS DEFINITELY A COLD WEATHER MENU!\nSummary: Omit the oregano and add chopped bell pepper, soft bread cubes, and egg\n--\nSummarize the suggestion:\nLovely way to serve Zucchini,its nice to able to prepare in advance so you can just pop it in the oven.I did substitute the green pepper for Red and half the chedder for a blue cheese(alocal on e here in S.Africa)just for a variation.\nSummary: Substitute the green pepper for red and half the cheddar for blue cheese\n--\nSummarize the suggestion:\nI cut back on the mayo, and made up the difference with sour cream to adjust the stiffness of the dip.\nSummary: Cut back on the mayo and make up the difference with sour cream\n--\nSummarize the suggestion:\nlove it, but without the bean sprouts.\nSummary: Don\'t include the bean sprouts\n--\nSummarize the suggestion:\nchewy goodness, not crispy at all. i even threw in craisins and left the oatmeal whole, and they were great.\nSummary: Add craisins and leave the oatmeal whole\n--\nSummarize the suggestion:\nthis is absolutely delicious. i even served it with lime slices so you could squeeze on more of the acid.\nSummary: Serve with lime slices\n--\nSummarize the suggestion:\nleeks on a pizza?! it was really delicious. i used a boboli and added some chicken sausage slices and mushrooms too.\nSummary: Add chicken sausage slices and mushrooms\n--\nSummarize the suggestion:\n'

app = Flask(__name__)
co = cohere.Client('wwgGM8zicRupgJVGxutU82I6IreIAsqyIMyuLYVa')

def scrape(url, n):

    # Search for recipe ID in URL with regex, which should be the last string
    string = r'[0-9]+'
    match = re.search(string, url[::-1])
    if not match:
        raise Exception("URL malformatted.")
    doc_id = match.group()[::-1]

    REVIEW_URL = "https://api.food.com/external/v1/recipes/XXX/feed?sort=-like&pn=YYY"
    review_url = REVIEW_URL.replace("XXX", doc_id)
    review_texts = []
    review_likes = []

    i = 1
    while True:

        # Stop after n searches
        if i >= n:
            break

        r = review_url.replace("YYY", str(i))
        print(r)

        # Call API to retrieve reviews
        page = requests.get(r)
        reviews = json.loads(page.text)
        reviews = reviews['data']['items']

        # Stop if there are no more reviews
        if len(reviews) == 0:
            break

        for review in reviews:
            try:
                review_texts.append(review['text'])
                review_likes.append(review['counts']['like'])
                #print(review['counts']['like'])
                #print(review['text'])
            except:
                continue

        i = i + 1
    return review_texts, review_likes

@app.route('/search')
def get_suggestions():

    args = request.args.to_dict()
    try:
        query = args['query']
        reviews, review_likes = scrape(query, 10)

        response = co.classify(
            model='large',
            inputs=reviews,
            examples=[Example("didnt say enough about how much of milk, sugar etc, needed to know how much, and if water bath for canning is needed", "0"), Example("Simple, but good. I make something similar for my nephew. He likes to dunk his in salsa.", "0"), Example("An excellent hearty meal...wonderful...too good....great recipe....Feel like eating up this page on Recipezaar right now!!!!!!!!!!!!!!!!!!!", "0"), Example("Our family found this recipe simply delicious and easy to make.", "0"), Example("My sons loved this,very quick ,simple and easy.I served them with a sweet and sour dip.I think I,ll double the amount next time as they went so quickly.", "0"), Example("This bread is easy and delicious!", "0"), Example("This was very easy to make and very good! It does make a big pot but beef stew is easy to freeze. I will definitely make again and keep in my recipe file.", "0"), Example("Thank you!!!!!!!! I might even celebrate Christmas...", "0"), Example("This dish is fabulous. we all loved it.", "0"), Example("I would be interested in knowing why the peppers were mushy and tasted more like vinegar - I am getting ready to pickle banana peppers - thank you.", "0"), Example("I think this is a decent bread recipe, but I think bread recipes with bread flour taste better. If ya don\'t have bread flour this is the way to go.", "0"), Example("This is similar to the halva I regularly make. I will post it soon:)", "0"), Example("These were a big hit. Very tasty and pretty easy to fix. Seems like something kids would like, too.", "0"), Example("Just the type recipe I came to this site for. I am going to take this to a Super Bowl party on Sunday", "0"), Example("Very Good! Everyone likes them.", "0"), Example("this is a fantastic dinner,lunch or a last minute solution to the familys hunger problems. i am very happy for the person who put this recipe on here thank you.", "0"), Example("The smell of this when its in the oven!....wow....this is delish!! =)", "0"), Example("My Grandma use to say that \"we ate everything, but the cluck\". I\'m sure that would include chicken feet!", "0"), Example("This dip is the best, great with fresh apple slices.", "0"), Example("I made this over the weekend and it was very good, although I have to agree getting the rub on was a bit messy. However I will definetly make it again and am sharing the recipe with friends!", "0"), Example("I\'m really going to try this one", "0"), Example("We are definitely macaroni hounds and this recipe,well\' in a word is awsome . You go girl and create more man pleasin\' vegan meals like this one. Oh yeah baby just one more helpin\' of this. \n \n \n \n  M.shane (ailsa\'s hubby)", "0"), Example("I have been using this recipie for a while now...its delish and a good winter standby when you can\'t think what too prepare for dinner. Even the kids love it.", "0"), Example("Wonderfully light texture. Delicious", "0"), Example("Great...I\'ve been looking for a decent bravas recipe for ages!!!", "0"), Example("I am really fond of this dish. It keeps well for leftovers - gets better even! Be careful on the amount of spices- I used too much cinnamon... Carol- for dummies like me you should put some approx amounts..", "0"), Example("Awesome!!! This is one f the best smooth salsa\'s I\'ve ever had!", "0"), Example("These were good.A good \'gingerbread\' flavor.Next time I will bake them in a smaller pan,they were pretty thin.They were nice to pack in the kids\' lunches", "0"), Example("My mother-in law was German add taught me how to make these 40 ye. ago. I make mine with onion and server them with ham and bean soup.", "1"), Example("Two eggs are not enough. I used three and it was still DRY (very tasty, but dry). Five or six would be much better - with two it was more like a pile of onions than an onion pie.", "1"), Example("I love butter but added almonds. Next time I\'ll try toasted almonds. IH", "1"), Example("I always mix my dressing ingredients together first before adding to the entire dish. For instance mix the mayo, salt, pepper, horseradish together first in a small dish. If you are usign small pieces of onion and celery too then add that in as well, Then mix all of that with the potatoes. It spreads all of the dressing ingredients better throughout the salad. Tastes better faster. Although it is always better to let it \"sit\" a bit before serving this helps speed up that process.", "1"), Example("This salad is absolutely delicious. My husband didn\'t like it, however, because he doesn\'t like cilantro. You could substitute parsley or leave it out entirely, if you wanted, but I like it the way it is. I will make this often and am sharing it with my friends!", "1"), Example("I agree with the other comments (use fresh mozerella, etc.) It\'s hard to find in some areas. Trader Joe\'s has it. Italian deli\'s have it, if you are lucky enough to have one where you live. I just have one suggestion. Drizzle on some Balsamic vinegar along with the olive oil. I travelled all over Italy last summer and ate this salad everywhere. Many places added the Balsamic and it makes a good salad really good!", "1"), Example("This was wonderful--finally got around to using the A to Z ingredients--and I used 2 cups of strawberries! this bread was great--it will be in my cookbook for good because of its totally unmatched level of versatility.", "1"), Example("Very easy to make for a lunch. I served it cold as a sandwich. I found it a little too bland though. Next time I make it I will add some cheese (like blue cheese or sharp cheddar)", "1"), Example("It is actually a recipe for Shrimp Mousse, it should be poured into a greased mold, refrigerated\n \n then unmolded onto a serving plate. It really would not freeze well because of the ingredients.", "1"), Example("Just like my Granny use to make but she.d swop raisins for currants occasionally.", "1"), Example("I did\'t have Mustard oil so used canola. Very tasty.", "1"), Example("Excellent easy recipe - I made w/out coconut and it was still good. Also, substituted oat flour for the oat meal and it worked just fine.", "1"), Example("Oh, what a great idea! phyllo dough and ground beef! I tried it with the cinnamon and stuff, and it tasted very Greek, like a pasticcio. I made another one without those 2 sweet spices, and it was more Italian. You can make a huge variation in the taste just by varying the spice mix a little bit.\n \n \n \n Yummy! I think I\'m gonna gain weight, but oh well, food is love.\n \n \n \n Please, post more recipes!!!", "1"), Example("This was VERY good, and easy. My favorite combination. There were no leftovers at our house either. I added a little minced garlic and I cooked the chicken in a baking dish in half a can of chicken broth, I didn\'t add the other ingredients until the chicken had cooked a little, then added the cheese, and diluted the soup with the other half can of broth. I also instead of \"topping\" the chicken with the stuffing mix, put it between and all around the chicken. That way, you could see the chicken, and the stuffing.", "1"), Example("I used small whole red potatoes instead of cutting up larger ones. Baked at 350 and added a little parsley for color. Absolutely delicious.", "1"), Example("I made this with breasts as well. I left the skin on (removing any excess fat) to avoid drying it out too much. It was great. I served it to my family and they all loved it. The left overs were even better the next day. Very easy, quick preparation and looks lovely served with saffron rice and fresh green beans. A great company dish.", "1"), Example("I substituted nutritional yeast for the milk powder to veganize this, and black instead of green olives, and it turned out absolutely fantastic.", "1"), Example("To me, basmati rice is the best. Instead of water I use chicken stock. It adds a little more flavor", "1"), Example("I made this and froze it. I served it a week later and it was just fine. Lemon and blueberries go together in this recipe very well", "1"), Example("This recipe needs to include some sliced carrots. I think they can be substituted for some of the peas, but they are definately something that needs to be added to break up the color a bit. About 1/2 cup should do.", "1"), Example("This was a very good meatloaf BUT to spicy for OUR TASTE. I omitted the oregano and garlic and added chopped bell pepper w/the onion. Added soft bread cubes to 2 tbs. milk, 1 tbs. Lea n Perrin, squished it all up well; added 1 well-beaten egg squishing more and squishing in about 3/4cup Ketchup. Patted into a 13x9 greased {Pam Spray} dish, w/hand made furrows across the top, laid raw sliced bacon strips on top. Baked at 325* to 350* about one (1) hour and drained grease/liquid from dish, removed bacon slices and poured{and spread evenly} about 1 cup Ketchup over top and continue cooking 30 minutes....my family love this version of this recipe.....especialy served with Dutchess Pototoes, dried Black-eyed peas, creamed corn, buttermilk cornbread and, if there is any room......Black-berry cobbler and vanilla ice cream.....THIS IS DEFINITELY A COLD WEATHER MENU!", "1"), Example("Lovely way to serve Zucchini,its nice to able to prepare in advance so you can just pop it in the oven.I did substitute the green pepper for Red and half the chedder for a blue cheese(alocal on e here in S.Africa)just for a variation.", "1")])
        #print('The confidence levels of the labels are: {}'.format(response.classifications[0].prediction))

        labels = []
        for classification in response.classifications:
            labels.append(int(classification.prediction))
         
        df = pd.DataFrame({
            'text': reviews,
            'likes': review_likes,
            })
        label_booleans = np.array(labels).astype(bool)
        df = df[label_booleans]
        df.sort_values('likes', ascending = False, inplace = True)
        top_5 = df[:5]
        top_5_texts = top_5['text']
        #print(top_5_texts)
        
        summaries = []
        original_reviews = []
        for text in top_5_texts:
            try:
                modified_prompt = prompt + text + "\nSummary:"

                summary = co.generate(
                    model='large',
                    prompt=modified_prompt,
                    max_tokens=30,
                    temperature=0.2,
                    k=0,
                    p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop_sequences=["--"],
                    return_likelihoods='NONE')

                print(summary.generations[0].text)

                summaries.append(summary.generations[0].text)
                original_reviews.append(text)
            except:
                continue
        
        return jsonify({'status': 1, 'summary': summaries, 'original_reviews': original_reviews})
    except:
        return jsonify({'status':0})
'''
'''